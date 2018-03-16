import cv2
import sys
import numpy as np
import time
import os

cap = cv2.VideoCapture(0)
bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')    #학습데이터 읽어오기
scaling_factor = 1.5            #윈도우 크기설정

prev_x = 0
prev_y = 0
prev_w = 0
prev_h = 0

def Read_TS():    #티셔츠 이미지 저장을 위한 함수
    T_Shirt1 = 'hoodT1_white.png'         #흰 티셔츠
    T_Shirt2 = 'T-Shirt_no.png'        #검은 티셔츠
    T_Shirt = [T_Shirt1, T_Shirt2]  #티셔츠 배열
    return T_Shirt

def Capture_Frame():  # 비디오 설정
    ret, frame = cap.read()
    frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_CUBIC)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # BGR-> Gray
    return frame, gray

def masked_Operation(x,y,w,h,frame,body_mask): # 상체 ROI의 범위를 정하고 이미지를 해당 영역에 덮어씌운다

    x = x-40
    y_offset = 220        # 이미지 사이즈 조정
    img_size = w +45

    frame_roi = frame[y+y_offset:y+y_offset+img_size, x:x+img_size]
    #cv2.imshow('video2',frame_roi)
    body_mask_small = cv2.resize(body_mask,(img_size,img_size),interpolation = cv2.INTER_CUBIC) # 옷이미지 키우기
    gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)#키운 이미지에 대한 mask (BGR->Gray)
   # if(i==2):
    #    ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY_INV) # 흰옷이 아닌경우

    #elif(i==1):
    ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY) # 흰옷일때

    mask_inv = cv2.bitwise_not(mask)

    masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask) # 오버레이되는 부분만 남게된다.
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv) #배경만 남게된다
    frame[y+y_offset:y+y_offset+img_size, x:x+img_size] = cv2.add(masked_body, masked_frame) # 화면에 이미지 오버레이


def Range_Operation(body,frame,body_mask):    # 예외범위를 추가한 코드
    count = 0
    global prev_x
    global prev_y
    global prev_w
    global prev_h

    for (x, y, w, h) in body:

        #print('x = ',x,'y = ',y,'w = ',w,'h = ',h)

        if (abs(prev_x-x) < 10) and (abs(prev_y-y) < 10): #이전 x,y 와 현재 x,y의 차이가 별로 나지 않으면 이전 위치의 이미지 출력
         #   print('prev_x =', prev_x, 'x = ', x, 'prev_y = ',prev_y, 'y = ', y, 'w= ',prev_w, 'h = ',prev_h)
            continue

        if (prev_w != 0):
            if (abs(prev_w-w) > 10) and (abs(prev_h-h) > 10):
          #      print('prev_w = ',prev_w,'w = ',w,'prev_h = ',prev_h,'h = ',h)
                continue

        count = count + 1
        if(count >= 2):
            break

        prev_x = x
        prev_y = y
        prev_w = w
        prev_h = h

        if  (x>120 and x<550 ):     # 특정 영역을 벗어나지 않으면 오버레이
            masked_Operation(x,y,w,h,frame,body_mask)

        else:         # 특정영역 벗어나면 continue
            continue


    if (count == 0):   # 이동 전, 후 차이가 적으면 이전 오버레이위치 출력
        if (prev_x !=0 and prev_y !=0 and prev_w != 0 and prev_h !=0):
            masked_Operation(prev_x,prev_y,prev_w,prev_h,frame,body_mask)

        #cv2.rectangle(frame,(prev_x,prev_y),(prev_x+prev_w,prev_y+prev_h),(0,255,255),2)
        #draw_shirt(x,y,w,h)

def Draw_Rect(frame,position,y1,y2,name):  # 카테고리 출력을 위한 함수
    font= cv2.FONT_HERSHEY_SIMPLEX
    Position=position
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2

    cv2.rectangle(frame, (750, y1), (950, y2), (255, 0, 0), 3)
    cv2.putText(frame, name,
        Position,
        font,
        fontScale,
        fontColor,
        lineType)

def Full_Overlay():       #이전에 정의했던 함수들을 모아서 처리
    # clothes - 1 overlay
    #os.system('sudo modprobe bcm2835-v4l2')

    T_Shirt=Read_TS()
    body_mask = cv2.imread(T_Shirt[0])  #T_Shirt배열 i 번째 이미지 읽어오기
    # h_mask, w_mask = body_mask.shape[:2] #이미지 영역

    if bodyCascade.empty(): #학습데이터 없을시 에러메세지
        raise IOError('Unable to load the mouth cascade classifier xml files')

    while True:
        # Capture frame-by-frame
        frame,gray=Capture_Frame()
        body = bodyCascade.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minSize=(100,200),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        Draw_Rect(frame,(800,210),160,260,'Reco')
        Draw_Rect(frame,(800,340),290,390,'List')
        Draw_Rect(frame,(800,470),420,520,'Buy')

        Range_Operation(body,frame,body_mask)


        cv2.imshow('video', frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
