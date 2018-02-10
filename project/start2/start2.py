import cv2
import sys
import numpy as np
import time
import os

cap = cv2.VideoCapture(0)
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
    #cv2.rectangle(frame, (450, 50), (570, 80), (255, 0, 0), 3)
    #cv2.rectangle(frame, (250, 50), (370, 80), (255, 0, 0), 3)
    #cv2.rectangle(frame, (50, 50), (170, 80), (255, 0, 0), 3)
    #cv2.circle(frame, (450,50), 40, (0,0,255), -1)

    

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
