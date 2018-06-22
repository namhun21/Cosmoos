import cv2
import sys
import numpy as np
import time
import os
import timeit

#김남훈 학생이 기본적인 구조를 만들었고 옷의 위치와 쓰레스 홀드를 정하는 코드는
#다같이 자세한 내용의 코드를 작성하였습니다.

def resetCount(*n):  # 가변인자를 이용하여 count들을 0으로 초기화 해주는 함수
    list1=[]
    for i in n:
        list1.append(0)
    return list1

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
def Menu_Click_Operation(name,roi, origraysc, count, Box_number):

    num = 0
    diff_image = cv2.absdiff(roi[Box_number],origraysc[Box_number])
    thresh, im_bw = cv2.threshold(diff_image,32,255,cv2.THRESH_BINARY)
    # for x in range(70):
    #     for y in range(70):
    #         oricolor = roi[Box_number][y, x]
    #         roicolor = origraysc[Box_number][y, x]
    #
    #         if (oricolor - roicolor < 30):    #달라진 정도가 30 미만이면 인식하지않는다
    #             roi[Box_number][y, x] = 0
    #
    #         else:
    #             roi[Box_number][y, x] = 255              #달라진 정도가 30 이상이면 인식한다
    #             num = num + 1

    cv2.imshow(name,im_bw)
    num = cv2.countNonZero(im_bw)
    if (num > 4900 * 0.5):      # 1번 영역에서 달라졌다고 인식한 수가 전체의 50%가 넘으면 그 영역 count를 1 더한다.
        count = count + 1

    return count

def overlay_Click_Operation(name,roi, origraysc, count, Box_number):

    num = 0
    diff_image = cv2.absdiff(roi[Box_number],origraysc[Box_number])
    thresh, im_bw = cv2.threshold(diff_image,30,255,cv2.THRESH_BINARY)

    # for x in range(60):
    #     for y in range(50):
    #         oricolor = roi[Box_number][y, x]
    #         roicolor = origraysc[Box_number][y, x]
    #
    #         if (oricolor - roicolor < 60):    #달라진 정도가 30 미만이면 인식하지않는다
    #             roi[Box_number][y, x] = 0
    #
    #         else:
    #             roi[Box_number][y, x] = 255              #달라진 정도가 30 이상이면 인식한다
    #             num = num + 1
    cv2.imshow(name,im_bw)
    num = cv2.countNonZero(im_bw)
    if (num > 3000 * 0.4):      # 1번 영역에서 달라졌다고 인식한 수가 전체의 40%가 넘으면 그 영역 count를 1 더한다.
        count = count + 1

    return count

def Select_Click_Operation(name, ButtonFrame,pictureButtonFrame):
    whiteNum = 0

    diff_image = cv2.absdiff(ButtonFrame, pictureButtonFrame)
    thresh, im_bw = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((3,3),np.uint8)
    # for x in range(width):
    #     for y in range(height):
    #        picturecolor = ButtonFrame[y,x]#현재 프레임의 오른쪽 버튼 부분
    #        ButtonFrameColor = pictureButtonFrame[y,x]#찍어놓은 이미지의 오른쪽 버튼 부분

           #if(picturecolor- ButtonFrameColor < 100):#비교해서 색의 차가 30 미만일 때
           #     ButtonFrame[y,x] = 0#흑색으로 변환
           #else:
           #     ButtonFrame[y,x] = 255#백색으로 변환
                # whiteNum = whiteNum+1#오른쪽 부분의 흰색 픽셀 개수 증가
    #erosion = cv2.erode(ButtonFrame,kernel,iterations=1)
    #dilation = cv2.dilate(ButtonFrame,kernel,iterations=1)
    # for x in range(width):
    #     for y in range(height):
    #         if(ButtonFrame[y,x] ==1):
    #             whiteNum = whiteNum + 1
    # if(cv2.countNonZero(im_bw) > width * height * 0.8):
    whiteNum = cv2.countNonZero(im_bw)
    if name is not None:
        cv2.imshow(name, im_bw)

    return whiteNum

def sizeUp(Clothes_name,img_size,Flag):  #옷의 이미지 크기 늘이기 위한 함수

    if Clothes_name.split("_")[3] == 'L':
        print('사이즈업 불가')
        return Clothes_name,img_size, Flag

    elif Clothes_name.split("_")[3] =='M':
        Clothes_name = Clothes_name.replace('M','L')
        img_size = img_size + 20
        Flag = 1
        return Clothes_name, img_size, Flag 
    elif Clothes_name.split("_")[3] =='S':
        Clothes_name = Clothes_name.replace('S','M')
        img_size = img_size + 20
        Flag = 1
        return Clothes_name,img_size, Flag

def sizeDown(Clothes_name,img_size,Flag):  #옷의 이미지 줄이기 위한 함수

    if Clothes_name.split("_")[3] == 'S':
        print('사이즈다운 불가')
        return Clothes_name,img_size, Flag
    elif Clothes_name.split("_")[3] =='M':
        Clothes_name = Clothes_name.replace('M','S')
        img_size = img_size - 20
        Flag = 2
        return Clothes_name, img_size, Flag
    elif Clothes_name.split("_")[3] =='L':
        Clothes_name = Clothes_name.replace('L','M')
        img_size = img_size - 20
        Flag = 2
        return Clothes_name, img_size, Flag

def Decision_mask(Clothes_name,gray_mask):

    Clothes_type = Clothes_name.split("_")[5]
    color = Clothes_name.split("_")[1]
    
    if(Clothes_type == 'basic'and color == 'gray'):
        ret, mask = cv2.threshold(gray_mask, 230,255, cv2.THRESH_BINARY_INV)
    elif( Clothes_type == 'basic'and color == 'white'):
        ret, mask = cv2.threshold(gray_mask, 1,255, cv2.THRESH_BINARY)
    elif(Clothes_type == 'basic' and color == 'beige'):
        ret, mask = cv2.threshold(gray_mask, 1,255, cv2.THRESH_BINARY)
    elif(Clothes_type == 'basic'and color == 'black'):
        ret, mask = cv2.threshold(gray_mask, 200,255, cv2.THRESH_BINARY_INV)
    elif(Clothes_type == 'basic'and color == 'blue'):
        ret, mask = cv2.threshold(gray_mask, 200,255, cv2.THRESH_BINARY_INV)
    elif(Clothes_type == 'stripe'and color =='black'):
        ret, mask = cv2.threshold(gray_mask, 1, 255, cv2.THRESH_BINARY)
    elif(Clothes_type == 'stripe'and color == 'blue'):
        ret, mask = cv2.threshold(gray_mask, 249, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'stripe'and color =='beige'):
        ret, mask = cv2.threshold(gray_mask, 252, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'dot'and color =='black'):
        ret, mask = cv2.threshold(gray_mask, 10, 255, cv2.THRESH_BINARY)
    elif (Clothes_type == 'dot'and color =='gray'):
        ret, mask = cv2.threshold(gray_mask, 245, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'dot'and color =='white'):
        ret, mask = cv2.threshold(gray_mask, 250, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'dot'and color =='blue'):
        ret, mask = cv2.threshold(gray_mask, 175, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'dot'and color =='beige'):
        ret, mask = cv2.threshold(gray_mask, 223, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'printing'and color == 'black'):
        ret, mask = cv2.threshold(gray_mask, 200, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'printing'and color == 'blue'):
        ret, mask = cv2.threshold(gray_mask, 254, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'printing'and color == 'beige'):
        ret, mask = cv2.threshold(gray_mask, 40, 255, cv2.THRESH_BINARY)
    elif (Clothes_type == 'printing'and color == 'white'):
        ret, mask = cv2.threshold(gray_mask, 1, 255, cv2.THRESH_BINARY)
    elif (Clothes_type == 'printing'and color == 'gray'):
        ret, mask = cv2.threshold(gray_mask, 30, 255, cv2.THRESH_BINARY)
    elif (Clothes_type == 'stripe'and color =='white'):
        ret, mask = cv2.threshold(gray_mask, 253, 255, cv2.THRESH_BINARY_INV)
    elif (Clothes_type == 'stripe'and color == 'gray'):
        ret, mask = cv2.threshold(gray_mask, 20 , 255, cv2.THRESH_BINARY)
    
    return mask

def Decision_sizeOffset(Clothes_name,x,y_offset, img_size):

    Clothes_type = Clothes_name.split("_")[5]
    color = Clothes_name.split("_")[1]
    
    if(Clothes_type == 'basic'and color == 'gray'):
        x = x- 3
        img_size = img_size + 30
        col = img_size + 10
    
        y_offset = 100
        
    elif( Clothes_type == 'basic'and color == 'white'):
        x = x-20
        y_offset = y_offset - 30
        img_size = img_size + 70
        col = img_size + 30

    elif(Clothes_type == 'basic' and color == 'beige'):
        img_size =img_size + 10
        col = img_size+55
        y_offset = 100

    elif(Clothes_type == 'basic'and color == 'black'):
        y_offset = 90
        img_size = img_size + 50
        x = x-20
        col = img_size

    elif(Clothes_type == 'basic'and color == 'blue'):
        x = x + 20
        img_size = img_size - 20
        col = img_size + 50
        y_offset = 100

    elif (Clothes_type == 'dot'and color =='black'):
        x = x + 30
        y_offset = 100
        img_size = img_size - 30
        col = img_size + 40

    elif (Clothes_type == 'dot'and color =='gray'):
        x = x + 25
        y_offset = 100
        img_size = img_size - 40
        col = img_size + 55

    elif (Clothes_type == 'dot'and color =='white'):
        x = x + 30
        y_offset = 110
        img_size = img_size
        col = img_size + 20

    elif (Clothes_type == 'dot'and color =='blue'):
        x = x + 10
        y_offset = 110
        img_size = img_size - 20
        col = img_size + 20

    elif (Clothes_type == 'dot'and color =='beige'):
        x = x + 5
        y_offset = 100
        img_size = img_size + 30
        col = img_size + 30

    elif (Clothes_type == 'printing'and color == 'black'):
        x = x-10 
        y_offset = 55
        img_size = img_size + 15
        col = img_size + 75

    elif (Clothes_type == 'printing'and color == 'blue'):
        x = x-21
        y_offset = 80
        img_size = img_size + 50
        col = img_size -10

    elif (Clothes_type == 'printing'and color == 'beige'):
        x = x + 20
        y_offset = 80
        img_size = img_size - 30
        col = img_size + 85

    elif (Clothes_type == 'printing'and color == 'white'):
        x = x +5
        y_offset = 122
        img_size = img_size - 10
        col = img_size + 20

    elif (Clothes_type == 'printing'and color == 'gray'):
        x = x - 12
        y_offset = 90
        img_size = img_size + 30
        col = img_size + 20

    elif (Clothes_type == 'stripe'and color =='white'):
        x = x + 20
        y_offset = 120
        img_size = img_size 
        col = img_size - 10

    elif (Clothes_type == 'stripe'and color == 'gray'):
        x = x + 15
        y_offset = 95
        img_size = img_size - 15
        col = img_size + 55
        
    elif(Clothes_type == 'stripe'and color =='black'):
        x = x+20
        y_offset = 95
        img_size = img_size
        col = img_size + 50

    elif(Clothes_type == 'stripe'and color == 'blue'):
        x = x +3
        y_offset = 100
        img_size = img_size + 15
        col = img_size + 10

    elif (Clothes_type == 'stripe'and color =='beige'):
        x = x+20
        y_offset = 90
        img_size = img_size-20
        col = img_size + 50


    return x, col, y_offset,img_size
