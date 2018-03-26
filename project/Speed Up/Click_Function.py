import cv2
import sys
import numpy as np
import time
import os
import timeit

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
def Click_Operation(roi, origraysc, waiting_time, count, num,Box_number):
    # num1 = 0
    # num2 = 0
    # num3 = 0
    start = timeit.default_timer()

    # waiting_time = 0

    # count1 = 0
    # count2 = 0
    # count3 = 0

    for x in range(120):
        for y in range(30):
            oricolor = roi[Box_number][y, x]
            roicolor = origraysc[Box_number][y, x]

            if (oricolor - roicolor < 30):    #달라진 정도가 30 미만이면 인식하지않는다
                roi[Box_number][y, x] = 0

            else:
                roi[Box_number][y, x] = 255              #달라진 정도가 30 이상이면 인식한다
                num = num + 1
                #print(num1)

    if (num > 3600 * 0.5):      # 1번 영역에서 달라졌다고 인식한 수가 전체의 50%가 넘으면 그 영역 count를 1 더한다.
        count = count + 1

    num = 0


    end = timeit.default_timer()

    #print((end-start)*1000)
    return count,num,waiting_time
