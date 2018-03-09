import cv2
import sys
import numpy as np
import time
import os

def draw_Click(frame, position, x1, x2, name):
    font = cv2.FONT_HERSHEY_SIMPLEX
    Position = position
    fontScale = 0.5
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.rectangle(frame, (x1, 50), (x2, 80), (255, 0, 0), 3)
    cv2.putText(frame, name,
                Position,
                font,
                fontScale,
                fontColor,
                lineType)


def make_Roi(gray, x1, y1):
    roi = gray[50:80, x1:y1]
    return roi


def Click_Operation(roi, origraysc, time, count1, count2, count3, num1,num2,num3):
    # num1 = 0
    # num2 = 0
    # num3 = 0

    # time = 0

    # count1 = 0
    # count2 = 0
    # count3 = 0

    for x in range(120):
        for y in range(30):
            oricolor1 = roi[0][y, x]
            roicolor1 = origraysc[0][y, x]
            oricolor2 = roi[1][y, x]
            roicolor2 = origraysc[1][y, x]
            oricolor3 = roi[2][y, x]
            roicolor3 = origraysc[2][y, x]

            if (oricolor1 - roicolor1 < 30):
                roi[0][y, x] = 0
               
            else:
                roi[0][y, x] = 255
                num1 = num1 + 1
                #print(num1)


            if (oricolor2 - roicolor2 < 30):
                roi[1][y, x] = 0
            else:
                roi[1][y, x] = 255
                num2 = num2 + 1
                #print(num2)

            if (oricolor3 - roicolor3 < 30):
                roi[2][y, x] = 0
            else:
                roi[2][y, x] = 255
                num3 = num3 + 1
            # print(num1,num2,num3)

    if (num1 > 3600 * 0.5 and time > 50):
        count1 = count1 + 1

    num1 = 0

    if (num2 > 3600 * 0.5 and time > 50):
        count2 = count2 + 1

    num2 = 0

    if (num3 > 3600 * 0.5 and time > 50):
        count3 = count3 + 1

    num3 = 0

    return count1, count2, count3,num1,num2,num3,time
