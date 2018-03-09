import cv2
import sys
import numpy as np
import time
import os
import UI_Start 
import UI_Recommand 
import Click_Function 


def Second_Menu(title,cap):
    #cap = cv2.VideoCapture(0)
    # Icon = ['T-Shirt.jpg','Y-Shirt.png','Hood.jpg']
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
    
    time = 0
    check = 0
    kernel = np.ones((5, 5), np.uint8)

    while True:
        ret, frame = cap.read()

        cv2.putText(frame,title,
                    bottomLeftCornerOfText_Title,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255,255,255),
                    2)

        Click_Function.draw_Click(frame, bottomLeftCornerOfText1, 450, 570, 'Recommand')
        Click_Function.draw_Click(frame, bottomLeftCornerOfText2, 250, 370, 'List')
        Click_Function.draw_Click(frame, bottomLeftCornerOfText3, 50, 170, 'Back')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        roi1 = Click_Function.make_Roi(gray, 450, 570)
        roi2 = Click_Function.make_Roi(gray, 250, 370)
        roi3 = Click_Function.make_Roi(gray, 50, 170)

        roi = [roi1, roi2, roi3]

        if (check == 0 and time > 100):
            #cap1 = cv2.VideoCapture(0)
            #ret, ori2 = cap1.read()

            # oriroi1 = ori2[50:80,450:570]
            # oriroi2 = ori2[50:80,250:370]
            # oriroi3 = ori2[50:80,50:170]

            origray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            origraysc1 = Click_Function.make_Roi(origray, 450, 570)
            origraysc2 = Click_Function.make_Roi(origray, 250, 370)
            origraysc3 = Click_Function.make_Roi(origray, 50, 170)

            origraysc = [origraysc1, origraysc2, origraysc3]

            check = 1

        if (check == 1):
            count1, count2, count3, num1,num2,num3, time = Click_Function.Click_Operation(roi, origraysc, time,count1,count2,count3,num1,num2,num3)

        print(count1, count2, count3)

        if (count1 > 20):
            print("success1")
            UI_Recommand.Third_Menu('Recommand',cap)
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count2 > 20):
            print("success2")
            UI_Recommand.Third_Menu('List',cap)
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count3 > 20):
            print("success3")
            UI_Start.First_Menu(cap)
            count1 = 0
            count2 = 0
            count3 = 0

        cv2.imshow('video', frame)
        time = time + 5

        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력 시 종료
            break
        elif cv2.waitKey(1) & 0xFF == ord('b'):  # b 입력 시 이전 페이지로 이동
            UI_Start.First_Menu(cap)

        elif cv2.waitKey(1) & 0xFF == ord('r'):  # r 입력 시 추천 페이지로 이동
            UI_Recommand.Third_Menu('Recommand',cap)

        elif cv2.waitKey(1) & 0xFF == ord('l'):  # l 입력 시 목록화면 페이지로 이동
            UI_Recommand.Third_Menu('List',cap)

    cv2.destroyAllWindows()
    cap.release()


