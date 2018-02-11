import cv2
import sys
import numpy as np
import time
import os
import Reco
import start1

def pou(Title):

    cap = cv2.VideoCapture(0)
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText_Title = (0,20)
    bottomLeftCornerOfText1 = (460,70)
    bottomLeftCornerOfText2 = (260,70)
    bottomLeftCornerOfText3 = (60,70)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.rectangle(frame, (450, 50), (570, 80), (255, 0, 0), 3)
        #cv2.rectangle(frame, (250, 50), (370, 80), (255, 0, 0), 3)
        #cv2.rectangle(frame, (50, 50), (170, 80), (255, 0, 0), 3)
        #cv2.circle(frame, (450,50), 40, (0,0,255), -1)

        #변수 a 에 start1에서 선택한 항목의 값 저장
        a = Title
        cv2.putText(frame,a,
            bottomLeftCornerOfText_Title,
            font,
            0.5,
            fontColor,
            lineType)

        cv2.putText(frame,'Reco',
            bottomLeftCornerOfText1,
            font,
            fontScale,
            fontColor,
            lineType)
        cv2.putText(frame,'List',
            bottomLeftCornerOfText2,
            font,
            fontScale,
            fontColor,
            lineType)
        cv2.putText(frame,'Back',
            bottomLeftCornerOfText3,
            font,
            fontScale,
            fontColor,
            lineType)


        cv2.imshow('video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('b'):
            start1.ping()
        elif cv2.waitKey(1) & 0xFF == ord('r'):
            Reco.recommand(a)
        elif cv2.waitKey(1) & 0xFF == ord('l'):
            Reco.recommand(a)







