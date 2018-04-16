import cv2
import sys
import numpy as np
import time
import os
import UI_Sub
import Function
import overlay

#recommend 화면은 임시로 만들었다 이상태로 구현되지 않을 것이다.


def Third_Menu(title,cap):
    #cap = cv2.VideoCapture(0)
    # Icon = ['T-Shirt.jpg','Y-Shirt.png','Hood.jpg']
    bottomLeftCornerOfText_Title = (0,20)
    bottomLeftCornerOfText1 = (460, 70)
    bottomLeftCornerOfText2 = (260, 70)
    bottomLeftCornerOfText3 = (60, 70)

    num1 = 0
    num2 = 0
    num3 = 0
    time = 0
    count1 = 0
    count2 = 0
    count3 = 0

    sum_time = 0
    n = 0
    waiting_time = 0
    check = 0
    kernel = np.ones((5, 5), np.uint8)

    while True:
        ret, frame = cap.read()
        #frame_copy = frame.copy()
        img = cv2.flip(frame,1)
        cv2.putText(img,'recommend',
                    bottomLeftCornerOfText_Title,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255,255,255),
                    2)
        Function.draw_Click(img, bottomLeftCornerOfText1, (450, 50), (570, 80), 'Wear')
        Function.draw_Click(img, bottomLeftCornerOfText2, (250, 50), (370, 80), 'Next')
        Function.draw_Click(img, bottomLeftCornerOfText3, (50, 50), (170, 80), 'Back')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        roi1 = Function.make_Roi(gray, 50 ,80 , 450, 570)
        roi2 = Function.make_Roi(gray, 50 ,80 , 250, 370)
        roi3 = Function.make_Roi(gray, 50 ,80 , 50, 170)

        roi = [roi1, roi2, roi3]

        if (check == 0 and time > 100):
            # cap1 = cv2.VideoCapture(0)
            # ret, ori2 = cap1.read()

            # oriroi1 = ori2[50:80,450:570]
            # oriroi2 = ori2[50:80,250:370]
            # oriroi3 = ori2[50:80,50:170]

            origray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            origraysc1 = Function.make_Roi(origray, 50 ,80 , 450, 570)
            origraysc2 = Function.make_Roi(origray, 50 ,80 , 250, 370)
            origraysc3 = Function.make_Roi(origray, 50 ,80 , 50, 170)

            origraysc = [origraysc1, origraysc2, origraysc3]

            check = 1

        if (check == 1):
            count1, num1, waiting_time = Function.Menu_Click_Operation(roi, origraysc, waiting_time, count1, num1, 0)
            count2, num2, waiting_time = Function.Menu_Click_Operation(roi, origraysc, waiting_time, count2, num2, 1)
            count3, num3, waiting_time = Function.Menu_Click_Operation(roi, origraysc, waiting_time, count3, num3, 2)

        #print(count3, count2, count1)

        if (count1 > 20):
            print("success1")
            #overlay.Full_Overlay()

        elif (count2 > 20):
            print("success2")
            #start2.pou('Y-shirt')

        elif (count3 > 20):
            print("success3")
            UI_Sub.Second_Menu(title,cap)


        cv2.imshow('video', img)
        time = time + 5


        #elif cv2.waitKey(1) & 0xFF == ord('t'):  # t 입력시 start2에 pou('T-shirt') 실행
            #start2.pou('T-shirt')

    cv2.destroyAllWindows()
    cap.release()


