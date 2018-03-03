#-*- coding: utf-8 -*-
import cv2
import sys
import numpy as np
import time
import os
import start2
import overlay

def recommand(a):

    cap = cv2.VideoCapture(0)
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText_Title = (0,20)
    bottomLeftCornerOfText1 = (460,70)
    bottomLeftCornerOfText2 = (260,70)
    bottomLeftCornerOfText3 = (60,70)
    fontScale              = 0.5
    fontColor              = (255,255,255)
    lineType               = 2
    num1 = 0
    num2 = 0
    num3 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    time = 0
    check = 0
    kernel = np.ones((5,5),np.uint8)
    
    while True:
        ret, frame = cap.read()
        #cv2.rectangle(frame, (450, 50), (570, 80), (255, 0, 0), 3)
        #cv2.rectangle(frame, (250, 50), (370, 80), (255, 0, 0), 3)
        #cv2.rectangle(frame, (50, 50), (170, 80), (255, 0, 0), 3)
        #cv2.circle(frame, (450,50), 40, (0,0,255), -1)
        img1 = frame.copy()
        
        roi1 = img1[50:80,450:570]
        roi2 = img1[50:80,250:370]
        roi3 = img1[50:80,50:170]

        roigray1 = cv2.cvtColor(roi1,cv2.COLOR_BGR2GRAY)
        roigray2 = cv2.cvtColor(roi2,cv2.COLOR_BGR2GRAY)
        roigray3 = cv2.cvtColor(roi3,cv2.COLOR_BGR2GRAY)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.rectangle(frame, (450, 50), (570, 80), (255, 0, 0), 3)
        cv2.rectangle(frame, (250, 50), (370, 80), (255, 0, 0), 3)
        cv2.rectangle(frame, (50, 50), (170, 80), (255, 0, 0), 3)
        #변수 a 에 start1에서 선택한 항목의 값 저장
        
        cv2.putText(frame,'Reco',
            bottomLeftCornerOfText_Title,
            font,
            0.5,
            fontColor,
            lineType)

        cv2.putText(frame, 'Wear',
            bottomLeftCornerOfText1,
            font,
            fontScale,
            fontColor,
            lineType)
        cv2.putText(frame, 'Next',
            bottomLeftCornerOfText2,
            font,
            fontScale,
            fontColor,
            lineType)
        cv2.putText(frame, 'Back',
            bottomLeftCornerOfText3,
            font,
            fontScale,
            fontColor,
            lineType)

        
        if(check == 0 and time > 100):
            cap1 = cv2.VideoCapture(0)
            ret, ori2 = cap1.read()

            oriroi1 = ori2[50:80,450:570]
            oriroi2 = ori2[50:80,250:370]
            oriroi3 = ori2[50:80,50:170]

            origray = cv2.cvtColor(ori2,cv2.COLOR_BGR2GRAY)

            origraysc1 = origray[50:80,450:570]
            origraysc2 = origray[50:80,250:370]
            origraysc3 = origray[50:80,50:170]

            #cv2.imshow('asdasdasdaq',origray)
            check = 1


        if(check == 1):
            for x in range(120):
                for y in range(30):
                  oricolor1 = roigray1[y,x]
                  roicolor1 = origraysc1[y,x]
                  oricolor2 = roigray2[y,x]
                  roicolor2 = origraysc2[y,x]
                  oricolor3 = roigray3[y,x]
                  roicolor3 = origraysc3[y,x]
                  if(oricolor1- roicolor1 < 30):
                       roi1[y,x] = 0
                  else:
                       roi1[y,x] = 255
                       num1 = num1+1
                  if(oricolor2- roicolor2 < 30):
                       roi2[y,x] = 0
                  else:
                       roi2[y,x] = 255
                       num2 = num2+1
                  if(oricolor3- roicolor3 < 30):
                       roi3[y,x] = 0
                  else:
                       roi3[y,x] = 255
                       num3 = num3+1

       # print(num1,num2,num3)


        if(num1 > 3600 * 0.5  and time > 50):

            count1 = count1+1

        num1 = 0

        if(num2 > 3600 * 0.5  and time > 50):

            count2 = count2+1


        num2 = 0

        if(num3 > 3600 * 0.5  and time > 50):

            count3 = count3+1


        num3 = 0

        print(count1, count2, count3)

        if(count1 > 30):
            print("success1")
            overlay.Full_Overlay()
            count1 = 0
            count2 = 0
            count3 = 0
        elif(count2 > 30):
            print("success2")
            pass
            count1 = 0
            count2 = 0
            count3 = 0
        elif(count3 > 30):
            print("success3")
            start2.pou('back')
            count1 = 0
            count2 = 0
            count3 = 0

        cv2.imshow('video', frame)
        time  = time + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):    # q 입력시 종료
            break
        elif cv2.waitKey(1) & 0xFF == ord('b'):  # b 입력시 start2 페이지로 이동
            start2.pou(a)
        elif cv2.waitKey(1) & 0xFF == ord('w'):  # w 입력시 overlay 화면으로 이동
            overlay.Full_Overlay()
        elif cv2.waitKey(1) & 0xFF == ord('n'):  # n 입력시 종료 추후 다른 추천 화면으로 넘어가도록 구현
            k = 3
            break


    cv2.destroyAllWindows()
    cap.release()





