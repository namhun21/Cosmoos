import cv2
import sys
import numpy as np
import time
import os
import UI_Start
import UI_Recommend
import Click_Function
import SelectClothes


def Second_Menu(title,cap):
    #cap = cv2.VideoCapture(0)
    # Icon = ['T-Shirt.jpg','Y-Shirt.png','Hood.jpg']
    #버튼 위치
    bottomLeftCornerOfText_Title = (0,20)
    bottomLeftCornerOfText1 = (460, 70)
    bottomLeftCornerOfText2 = (260, 70)
    bottomLeftCornerOfText3 = (60, 70)

    num1 = 0
    num2 = 0
    num3 = 0

    count1 = 0
    count2 = 0
    count3 = 0

    waiting_time = 0
    check = 0
    kernel = np.ones((5, 5), np.uint8)

    while True:
        ret, frame = cap.read()
        img = cv2.flip(frame,1)

        cv2.putText(img,title,
                    bottomLeftCornerOfText_Title,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255,255,255),
                    2)
        #클릭 버튼
        Click_Function.draw_Click(img, bottomLeftCornerOfText1, (450, 50), (570, 80), 'Recommand')
        Click_Function.draw_Click(img, bottomLeftCornerOfText2, (250, 50), (370, 80), 'List')
        Click_Function.draw_Click(img, bottomLeftCornerOfText3, (50, 50), (170, 80), 'Back')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        roi1 = Click_Function.make_Roi(gray, 50 ,80 ,450 , 570)
        roi2 = Click_Function.make_Roi(gray, 50 ,80, 250, 370)
        roi3 = Click_Function.make_Roi(gray, 50 ,80, 50, 170)

        roi = [roi1, roi2, roi3]

        if (check == 0 and waiting_time > 100):    #클릭 구현시 필요한 사진
            #cap1 = cv2.VideoCapture(0)
            #ret, ori2 = cap1.read()

            # oriroi1 = ori2[50:80,450:570]
            # oriroi2 = ori2[50:80,250:370]
            # oriroi3 = ori2[50:80,50:170]

            origray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            origraysc1 = Click_Function.make_Roi(origray,50 ,80 ,450, 570)
            origraysc2 = Click_Function.make_Roi(origray,50 ,80, 250, 370)
            origraysc3 = Click_Function.make_Roi(origray,50 ,80, 50, 170)

            origraysc = [origraysc1, origraysc2, origraysc3]

            check = 1

        if (check == 1):    #클릭 함수 실행
            count1, num1, waiting_time = Click_Function.Click_Operation(roi, origraysc, waiting_time, count1, num1, 0)
            count2, num2, waiting_time = Click_Function.Click_Operation(roi, origraysc, waiting_time, count2, num2, 1)
            count3, num3, waiting_time = Click_Function.Click_Operation(roi, origraysc, waiting_time, count3, num3, 2)

        print(count3, count2, count1)

        if (count1 > 20):               #count1이 20 초과하면 UI_Recommand에 있는 Third_Menu(title)실행
            print("success1")
            UI_Recommend.Third_Menu(title,cap)   #Third_Menu에 title를 가져가야 Third_Menu에서 다시 Second_Menu로 돌아올때 title을 가져다 쓸 수 있다
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count2 > 20):
            print("success2")
            SelectClothes.SelectClothes(cap)   #list
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count3 > 20):
            print("success3")
            UI_Start.First_Menu(cap)
            count1 = 0
            count2 = 0
            count3 = 0

        cv2.imshow('video', img)
        waiting_time = waiting_time + 5

        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력 시 종료
            break
        elif cv2.waitKey(1) & 0xFF == ord('b'):  # b 입력 시 이전 페이지로 이동
            UI_Start.First_Menu(cap)

        elif cv2.waitKey(1) & 0xFF == ord('r'):  # r 입력 시 추천 페이지로 이동
            UI_Recommend.Third_Menu(title,cap)

        elif cv2.waitKey(1) & 0xFF == ord('l'):  # l 입력 시 목록화면 페이지로 이동
            SelectClothes.SelectClothes(cap)

    cv2.destroyAllWindows()
    cap.release()

