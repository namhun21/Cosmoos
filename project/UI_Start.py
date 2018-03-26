import cv2
import sys
import numpy as np
import time
import os
import UI_Sub
import Click_Function
import time_measurement

def First_Menu(cap):


    # Icon = ['T-Shirt.jpg','Y-Shirt.png','Hood.jpg']
    #버튼 위치
    bottomLeftCornerOfText1 = (460, 70)
    bottomLeftCornerOfText2 = (260, 70)
    bottomLeftCornerOfText3 = (60, 70)


    count1 = 0
    count2 = 0
    count3 = 0

    num1 = 0
    num2 = 0
    num3 = 0
    sum_time = 0
    n = 0

    waiting_time = 0
    check = 0
    kernel = np.ones((5, 5), np.uint8)

    while True:
        First_Menu_startTime = int(round(time.time() * 1000))

        ret, frame = cap.read()
        img = cv2.flip(frame,1)
        #frame_copy = frame.copy()

        #클릭 버튼 만들기
        Click_Function.draw_Click(img, bottomLeftCornerOfText1, (450, 50), (570, 80), 'T-shirt')
        Click_Function.draw_Click(img, bottomLeftCornerOfText2, (250, 50), (370, 80), 'Y-shirt')
        Click_Function.draw_Click(img, bottomLeftCornerOfText3, (50, 50), (170, 80), 'Hood')


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        roi1 = Click_Function.make_Roi(gray,50 ,80 ,450, 570)
        roi2 = Click_Function.make_Roi(gray,50 ,80 ,250, 370)
        roi3 = Click_Function.make_Roi(gray,50 ,80 ,50, 170)

        roi = [roi1, roi2, roi3]

        if (check == 0 and waiting_time > 100):   # waiting_time이 100이상이되면 버튼 클릭 인식을 시작한다.
                                          # 사진을 찍어서 지금 화면과 달라지는 영역을 인식한다.
            # cap1 = cv2.VideoCapture(0)
            # ret, ori2 = cap1.read()

            # oriroi1 = ori2[50:80,450:570]
            # oriroi2 = ori2[50:80,250:370]
            # oriroi3 = ori2[50:80,50:170]

            origray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            origraysc1 = Click_Function.make_Roi(origray,50 ,80 , 450, 570)
            origraysc2 = Click_Function.make_Roi(origray,50 ,80 , 250, 370)
            origraysc3 = Click_Function.make_Roi(origray,50 ,80 , 50, 170)

            origraysc = [origraysc1, origraysc2, origraysc3]

            check = 1


        if (check == 1):    #클릭 함수를 실행시킨다
            
            count1, count2, count3, num1,num2,num3, waiting_time = Click_Function.Click_Operation(roi, origraysc, waiting_time,count1,count2,count3,num1,num2,num3)



        #print(count3, count2, count1)

        if (count1 > 20):         #count1이 20이 넘으면 UI_Sub에 있는 Second_Menu를 실행시킨다.
            print("success1")
            UI_Sub.Second_Menu('T-shirt',cap)
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count2 > 20):
            print("success2")
            UI_Sub.Second_Menu('Y-shirt',cap)
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count3 > 20):
            print("success3")
            UI_Sub.Second_Menu('Hood-T',cap)
            count1 = 0
            count2 = 0
            count3 = 0

        cv2.imshow('video', img)
        
        waiting_time = waiting_time + 5

        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력시 종료
            break
        elif cv2.waitKey(1) & 0xFF == ord('h'):  # h 입력시 UI_Sub에 Second_Menu('Hood-T') 실행
            UI_Sub.Second_Menu('Hood-T',cap)

        elif cv2.waitKey(1) & 0xFF == ord('y'):  # y 입력시 UI_Sub에 Second_Menu('Y-shirt') 실행
            UI_Sub.Second_Menu('Y-shirt',cap)

        elif cv2.waitKey(1) & 0xFF == ord('t'):  # t 입력시 UI_Sub에 Second_Menu('T-shirt') 실행
            UI_Sub.Second_Menu('T-shirt',cap)

        First_Menu_endTime = int(round(time.time() * 1000))

        sum_time,n = time_measurement.measure(First_Menu_startTime, First_Menu_endTime, sum_time, n)
        


    cv2.destroyAllWindows()
    cap.release()




