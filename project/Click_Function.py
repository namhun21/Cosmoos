import cv2
import sys
import numpy as np
import time
import os

def draw_Click(frame, position, S_Range, E_Range, name):   #클릭하는 버튼의 인터페이스를 구현한다
    font = cv2.FONT_HERSHEY_SIMPLEX
    Position = position
    fontScale = 0.5
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.rectangle(frame, S_Range, E_Range, (255, 0, 0), 3)
    cv2.putText(frame, name,
                Position,
                font,
                fontScale,
                fontColor,
                lineType)


def make_Roi(gray, y1, y2, x1, x2):     #일정 영역을 gray한다
    roi = gray[y1:y2, x1:x2]
    return roi


#클릭하는 동작
#지금화면과 이전화면을 비교하여 달라진 영역을 계산하여 일정 수준 이상 달라져 있으면 클릭이 되게한다
def Click_Operation(roi, origraysc, waiting_time, count1, count2, count3, num1,num2,num3):
    # num1 = 0
    # num2 = 0
    # num3 = 0

    # waiting_time = 0

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

            if (oricolor1 - roicolor1 < 30):    #달라진 정도가 30 미만이면 인식하지않는다
                roi[0][y, x] = 0

            else:
                roi[0][y, x] = 255              #달라진 정도가 30 이상이면 인식한다
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

    if (num1 > 3600 * 0.5):      # 1번 영역에서 달라졌다고 인식한 수가 전체의 50%가 넘으면 그 영역 count를 1 더한다.
        count1 = count1 + 1

    num1 = 0

    if (num2 > 3600 * 0.5):
        count2 = count2 + 1

    num2 = 0

    if (num3 > 3600 * 0.5):
        count3 = count3 + 1

    num3 = 0

    return count1, count2, count3,num1,num2,num3,waiting_time
