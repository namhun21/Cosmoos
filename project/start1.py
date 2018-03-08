import cv2
import sys
import numpy as np
import time
import os
import start2

def ping():

    cap = cv2.VideoCapture(0)
    #Icon = ['T-Shirt.jpg','Y-Shirt.png','Hood.jpg']
    font                   = cv2.FONT_HERSHEY_SIMPLEX
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
        img1 = frame.copy()

        roi1 = img1[50:80,450:570]
        roi2 = img1[50:80,250:370]
        roi3 = img1[50:80,50:170]

        roigray1 = cv2.cvtColor(roi1,cv2.COLOR_BGR2GRAY)
        roigray2 = cv2.cvtColor(roi2,cv2.COLOR_BGR2GRAY)
        roigray3 = cv2.cvtColor(roi3,cv2.COLOR_BGR2GRAY)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        #icon_mask1 = cv2.imread(Icon[0]) # T-shirt 아이콘
        #icon_mask2 = cv2.imread(Icon[1]) # Y-shirt 아이콘
        #icon_mask3 = cv2.imread(Icon[2]) # Hood 아이콘

        cv2.rectangle(frame, (450, 50), (570, 80), (255, 0, 0), 3)
        cv2.rectangle(frame, (250, 50), (370, 80), (255, 0, 0), 3)
        cv2.rectangle(frame, (50, 50), (170, 80), (255, 0, 0), 3)


        #frame_roi_1 = frame[10:60, 460:510]
        #frame_roi_2 = frame[10:60, 260:310]
        #frame_roi_3 = frame[10:60, 60:110]

        #icon_mask_small_1 = cv2.resize(icon_mask1, (50, 50), interpolation=cv2.INTER_AREA)
        #icon_mask_small_2 = cv2.resize(icon_mask2, (50, 50), interpolation=cv2.INTER_AREA)
        #icon_mask_small_3 = cv2.resize(icon_mask3, (50, 50), interpolation=cv2.INTER_AREA)

        #gray_mask_1 = cv2.cvtColor(icon_mask_small_1, cv2.COLOR_BGR2GRAY)  # 키운 이미지에 대한 mask (BGR->Gray)
        #ret, mask1 = cv2.threshold(gray_mask_1, 127, 255, cv2.THRESH_BINARY_INV)  #T-shirt
        #mask_inv1 = cv2.bitwise_not(mask1)
        #masked_icon1 = cv2.bitwise_and(icon_mask_small_1,icon_mask_small_1,mask=mask1)
        #masked_frame1 = cv2.bitwise_and(frame_roi_1,frame_roi_1,mask=mask_inv1)
        #frame[10:60,460:510] = cv2.add(masked_icon1, masked_frame1)

        #gray_mask_2 = cv2.cvtColor(icon_mask_small_2, cv2.COLOR_BGR2GRAY)  # 키운 이미지에 대한 mask (BGR->Gray)
        #ret, mask2 = cv2.threshold(gray_mask_2, 140, 255, cv2.THRESH_BINARY)  #Y-shirt
        #mask_inv2 = cv2.bitwise_not(mask2)
        #masked_icon2 = cv2.bitwise_and(icon_mask_small_2, icon_mask_small_2, mask=mask2)
        #masked_frame2 = cv2.bitwise_and(frame_roi_2, frame_roi_2, mask=mask_inv2)
        #frame[10:60, 260:310] = cv2.add(masked_icon2, masked_frame2)

        #gray_mask_3 = cv2.cvtColor(icon_mask_small_3, cv2.COLOR_BGR2GRAY)  # 키운 이미지에 대한 mask (BGR->Gray)
        #ret, mask3 = cv2.threshold(gray_mask_3, 127, 255, cv2.THRESH_BINARY_INV)  # Hood
        #mask_inv3 = cv2.bitwise_not(mask3)
        #masked_icon3 = cv2.bitwise_and(icon_mask_small_3, icon_mask_small_3, mask=mask3)
        #masked_frame3 = cv2.bitwise_and(frame_roi_3, frame_roi_3, mask=mask_inv3)
        #frame[10:60, 60:110] = cv2.add(masked_icon3, masked_frame3)



        cv2.putText(frame,'T-shirt',
            bottomLeftCornerOfText1,
            font,
            fontScale,
            fontColor,
            lineType)
        cv2.putText(frame,'Y-shirt',
            bottomLeftCornerOfText2,
            font,
            fontScale,
            fontColor,
            lineType)
        cv2.putText(frame,'Hood-T',
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

        if(count1 > 20):
            print("success1")
            start2.pou('T-shirt')
            count1 = 0
            count2 = 0
            count3 = 0
        elif(count2 > 20):
            print("success2")
            start2.pou('Y-shirt')
            count1 = 0
            count2 = 0
            count3 = 0
        elif(count3 > 20):
            print("success3")
            start2.pou('Hood-T')
            count1 = 0
            count2 = 0
            count3 = 0


        cv2.imshow('video', frame)
        time  = time + 5

        if cv2.waitKey(1) & 0xFF == ord('q'):      #q 입력시 종료
            break
        elif cv2.waitKey(1) & 0xFF == ord('h'):    # h 입력시 start2에 pou('Hood-T') 실행
            start2.pou('Hood-T')

        elif cv2.waitKey(1) & 0xFF == ord('y'):    # y 입력시 start2에 pou('Y-shirt') 실행
            start2.pou('Y-shirt')

        elif cv2.waitKey(1) & 0xFF == ord('t'):    # t 입력시 start2에 pou('T-shirt') 실행
            start2.pou('T-shirt')


    cv2.destroyAllWindows()
    cap.release()

