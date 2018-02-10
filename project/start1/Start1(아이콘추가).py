import cv2
import sys
import numpy as np
import time
import os

cap = cv2.VideoCapture(0)
Icon = ['T-Shirt.jpg','Y-Shirt.png','Hood.jpg']
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText1 = (460,70)
bottomLeftCornerOfText2 = (260,70)
bottomLeftCornerOfText3 = (60,70)
fontScale              = 0.5
fontColor              = (255,255,255)
lineType               = 2


while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    icon_mask1 = cv2.imread(Icon[0]) # T-shirt 아이콘
    icon_mask2 = cv2.imread(Icon[1]) # Y-shirt 아이콘
    icon_mask3 = cv2.imread(Icon[2]) # Hood 아이콘

    # cv2.rectangle(frame, (450, 50), (570, 80), (255, 0, 0), 3)
    # cv2.rectangle(frame, (250, 50), (370, 80), (255, 0, 0), 3)
    # cv2.rectangle(frame, (50, 50), (170, 80), (255, 0, 0), 3)


    frame_roi_1 = frame[10:60, 460:510]
    frame_roi_2 = frame[10:60, 260:310]
    frame_roi_3 = frame[10:60, 60:110]

    icon_mask_small_1 = cv2.resize(icon_mask1, (50, 50), interpolation=cv2.INTER_AREA)
    icon_mask_small_2 = cv2.resize(icon_mask2, (50, 50), interpolation=cv2.INTER_AREA)
    icon_mask_small_3 = cv2.resize(icon_mask3, (50, 50), interpolation=cv2.INTER_AREA)

    gray_mask_1 = cv2.cvtColor(icon_mask_small_1, cv2.COLOR_BGR2GRAY)  # 키운 이미지에 대한 mask (BGR->Gray)
    ret, mask1 = cv2.threshold(gray_mask_1, 127, 255, cv2.THRESH_BINARY_INV)  # T-Shirt
    mask_inv1 = cv2.bitwise_not(mask1)
    masked_icon1 = cv2.bitwise_and(icon_mask_small_1,icon_mask_small_1,mask=mask1)
    masked_frame1 = cv2.bitwise_and(frame_roi_1,frame_roi_1,mask=mask_inv1)
    frame[10:60,460:510] = cv2.add(masked_icon1, masked_frame1)

    gray_mask_2 = cv2.cvtColor(icon_mask_small_2, cv2.COLOR_BGR2GRAY)  # 키운 이미지에 대한 mask (BGR->Gray)
    ret, mask2 = cv2.threshold(gray_mask_2, 140, 255, cv2.THRESH_BINARY)  # 흰옷일때
    mask_inv2 = cv2.bitwise_not(mask2)
    masked_icon2 = cv2.bitwise_and(icon_mask_small_2, icon_mask_small_2, mask=mask2)
    masked_frame2 = cv2.bitwise_and(frame_roi_2, frame_roi_2, mask=mask_inv2)
    frame[10:60, 260:310] = cv2.add(masked_icon2, masked_frame2)

    gray_mask_3 = cv2.cvtColor(icon_mask_small_3, cv2.COLOR_BGR2GRAY)  # 키운 이미지에 대한 mask (BGR->Gray)
    ret, mask3 = cv2.threshold(gray_mask_3, 127, 255, cv2.THRESH_BINARY_INV)  # 흰옷일때
    mask_inv3 = cv2.bitwise_not(mask3)
    masked_icon3 = cv2.bitwise_and(icon_mask_small_3, icon_mask_small_3, mask=mask3)
    masked_frame3 = cv2.bitwise_and(frame_roi_3, frame_roi_3, mask=mask_inv3)
    frame[10:60, 60:110] = cv2.add(masked_icon3, masked_frame3)



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

    
    cv2.imshow('vedio', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
cap.release()
