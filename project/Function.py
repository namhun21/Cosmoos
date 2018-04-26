import cv2
import sys
import numpy as np
import time
import os
import timeit

def resetCount(*n):
    list1=[]
    for i in n:
        list1.append(0)
    return list1

def draw_Click(frame, position, S_Range, E_Range, name):   #클릭하는 버튼의 인터페이스를 구현한다
    #millis_start = int(round(time.time()*1000))
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

    #millis_end = int(round(time.time() * 1000))
    #print("draw_click : ",millis_end - millis_start,"ms")



def make_Roi(gray, y1, y2, x1, x2):     #일정 영역을 gray한다
    #millis_start = int(round(time.time() * 1000))
    roi = gray[y1:y2, x1:x2]
    #millis_end = int(round(time.time() * 1000))
    #print("make_roi : ",millis_end - millis_start,"ms")
    return roi


#클릭하는 동작
#지금화면과 이전화면을 비교하여 달라진 영역을 계산하여 일정 수준 이상 달라져 있으면 클릭이 되게한다
def Menu_Click_Operation(roi, origraysc, count,Box_number):
    # num1 = 0
    # num2 = 0
    # num3 = 0

    # waiting_time = 0

    # count1 = 0
    # count2 = 0
    # count3 = 0
    num = 0
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



    #print((end-start)*1000)
    return count

def overlay_Click_Operation(roi, origraysc, count, num,Box_number):
    # num1 = 0
    # num2 = 0
    # num3 = 0

    # waiting_time = 0

    # count1 = 0
    # count2 = 0
    # count3 = 0

    for x in range(100):
        for y in range(50):
            oricolor = roi[Box_number][y, x]
            roicolor = origraysc[Box_number][y, x]

            if (oricolor - roicolor < 30):    #달라진 정도가 30 미만이면 인식하지않는다
                roi[Box_number][y, x] = 0

            else:
                roi[Box_number][y, x] = 255              #달라진 정도가 30 이상이면 인식한다
                num = num + 1
                #print(num1)

    if (num > 5000 * 0.5):      # 1번 영역에서 달라졌다고 인식한 수가 전체의 50%가 넘으면 그 영역 count를 1 더한다.
        count = count + 1

    num = 0


    #print((end-start)*1000)
    return count,num

def Select_Click_Operation(ButtonFrame,pictureButtonFrame,width,height):
    whiteNum = 0
    for x in range(width):
        for y in range(height):
           picturecolor = ButtonFrame[y,x]#현재 프레임의 오른쪽 버튼 부분
           ButtonFrameColor = pictureButtonFrame[y,x]#찍어놓은 이미지의 오른쪽 버튼 부분
           if(picturecolor- ButtonFrameColor < 30):#비교해서 색의 차가 30 미만일 때
                ButtonFrame[y,x] = 0#흑색으로 변환
           else:
                ButtonFrame[y,x] = 255#백색으로 변환
                whiteNum = whiteNum+1#오른쪽 부분의 흰색 픽셀 개수 증가

    return whiteNum

def sizeUp(Clothes_name,img_size):  #옷의 이미지 크기 늘이기 위한 함수

    if Clothes_name.split("_")[3] == 'L':
        print('사이즈업 불가')
        return Clothes_name,img_size

    elif Clothes_name.split("_")[3] =='M':
        Clothes_name = Clothes_name.replace('M','L')
        img_size = img_size + 20
        return Clothes_name, img_size
    elif Clothes_name.split("_")[3] =='S':
        Clothes_name = Clothes_name.replace('S','M')
        img_size = img_size + 20
        return Clothes_name,img_size

def sizeDown(Clothes_name,img_size):  #옷의 이미지 줄이기 위한 함수

    if Clothes_name.split("_")[3] == 'S':
        print('사이즈다운 불가')
        return Clothes_name,img_size
    elif Clothes_name.split("_")[3] =='M':
        Clothes_name = Clothes_name.replace('M','S')
        img_size = img_size - 20
        return Clothes_name, img_size
    elif Clothes_name.split("_")[3] =='L':
        Clothes_name = Clothes_name.replace('L','M')
        img_size = img_size - 20
        return Clothes_name, img_size
