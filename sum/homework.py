import cv2
import sys
import numpy as np
import time
import os


def Read_TS():    #티셔츠 이미지 저장을 위한 함수
    T_Shirt1 = 'hoodT1.png'         #흰 티셔츠
    T_Shirt2 = 'T-Shirt.png'        #검은 티셔츠
    T_Shirt = [T_Shirt1, T_Shirt2]  #티셔츠 배열
    return T_Shirt

def Capture_Frame():  # 비디오 설정 
    ret, frame = cap.read() 
    frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # BGR-> Gray
    return frame, gray

prev_x = 0
prev_y = 0
prev_w = 0
prev_h = 0


def Operation(body,frame,body_mask,i):
    count = 0
    global prev_x
    global prev_y
    global prev_w
    global prev_h
    for (x, y, w, h) in body:

        if (abs(prev_x-x) < 10) and (abs(prev_y-y) < 10):
            print('prev_x =', prev_x, 'x = ', x, 'prev_y = ',prev_y, 'y = ', y, 'w= ',prev_w, 'h = ',prev_h)
            continue

        if (prev_w != 0):
            if (abs(prev_w-w) > 20) and (abs(prev_h-h) > 20):
                continue
        
        count = count + 1
        if(count >= 2):
            break

        prev_x = x
        prev_y = y
        prev_w = w
        prev_h = h
        
        x = x-40        
        img_size = w + 50
        y_offset = 220

        frame_roi = frame[y+y_offset:y+y_offset+img_size, x:x+img_size]
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        
        body_mask_small = cv2.resize(body_mask,(img_size,img_size),interpolation = cv2.INTER_AREA) # 옷이미지 키우기
        gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)#키운 이미지에 대한 mask (BGR->Gray)
       
        if(i==2):
            ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY_INV) # 흰옷이 아닌경우
            
        elif(i==1):
            ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY) # 흰옷일때

        mask_inv = cv2.bitwise_not(mask)

        if(x<50 or x>620 or y>250):     #영역 벗어나는거 제외
            continue
        else:
            #draw_shirt(w,y,w,h)
            masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask) # 오버레이되는 부분만 남게된다.
            masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv) #배경만 남게된다
            frame[y+y_offset:y+y_offset+img_size, x:x+img_size] = cv2.add(masked_body, masked_frame) # 화면에 이미지 오버레이
            #cv2.rectangle(frame, (x, y+150), (x+300 ,y+450), (0, 0, 255), 2)

            
    if (count == 0):
        cv2.rectangle(frame,(prev_x,prev_y),(prev_x+prev_w,prev_y+prev_h),(0,255,255),2)
        #draw_shirt(x,y,w,h)
        

 
def draw_Fist(x,y,w,h,frame,count):
    if(w>30 and h>25):
        if ((x>450 and y>50) and (x<600 and y<150)) or ((x>50 and y>50) and (x<200 and y<150)): # 주먹이 사각형 범위 안에 있을때만 검출
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        if((int)((2*x+w)/2)> 100 and (int)((2*x+w)/2) < 200 and (int)((2*y+h)/2) > 150 and (int)((2*y+h)/2) < 250):
            count = count + 1

            
def overlay(i):       #i 번째 옷 오버레이하는 정의 함수
    # clothes - 1 overlay 
    os.system('sudo modprobe bcm2835-v4l2') 
    count = 0                   #오버레이 화면에서 빠져나올때 사용하는 변수

    T_Shirt=Read_TS()
    body_mask = cv2.imread(T_Shirt[i-1])  #T_Shirt배열 i 번째 이미지 읽어오기
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
        cv2.imshow('origin',frame)
        cv2.imshow('gray',gray)
        # Draw a rectangle around the faces
        Operation(body,frame,body_mask,i)
        

        fistList = fist_pattern.detectMultiScale(gray, 1.5)
        cv2.rectangle(frame, (100, 150), (200, 250), (255, 0, 0), 3)

        for (x, y, w, h) in fistList:       #주먹 인식해서 해당 네모에 있을때 초기화면으로 감 변수명 신경 안써도됨
            draw_Fist(x,y,w,h,frame,count)
                                 
                                     
        cv2.imshow('Video1', frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
            
        if(count>20):
            break

    cv2.destroyAllWindows()
    
def Show_Button():
    frame,gray=Capture_Frame()
    fistList = fist_pattern.detectMultiScale(gray, 1.5)
    cv2.rectangle(frame, (450, 50), (600, 150), (255, 0, 0), 3)
    cv2.rectangle(frame, (50, 50), (200, 150), (255, 0, 0), 3)
    return frame,fistList


def CountNum(x,y,w,h,frame):
    global count1
    global count2
    if(w>30 and h>25):
        if ((x>450 and y>50) and (x<600 and y<150)) or ((x>50 and y>50) and (x<200 and y<150)): # 주먹이 사각형 범위 안에 있을때만 검출
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                   
                
        if((int)((2*x+w)/2)> 50 and (int)((2*x+w)/2) < 200 and (int)((2*y+h)/2) > 50 and (int)((2*y+h)/2) < 150):
            count1 = count1 + 1
                        
        elif((int)((2*x+w)/2)> 400 and (int)((2*x+w)/2) < 600 and (int)((2*y+h)/2) > 50 and (int)((2*y+h)/2) < 150):
            count2 = count2 + 1


num = 0                         #화면 전환에 필요한 변수
count1 = 0                      #1번 옷을 선택할때 사용하는 변수
count2 = 0                      #2번 옷을 선택할때 사용하는 변수

cap = cv2.VideoCapture(0)
fist_pattern = cv2.CascadeClassifier('fist.xml')    #학습데이터 읽어오기
bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')    #학습데이터 읽어오기
scaling_factor = 1.5            #윈도우 크기설정


#실제 실행 화면 코드
while True:
    if num==0:
        while True:
            frame,fistList=Show_Button()

            for (x, y, w, h) in fistList:
                CountNum(x,y,w,h,frame)

            cv2.imshow('image', frame)
            
            if cv2.waitKey(1) and 0xFF == ord('q'):
                break
            
            if(count1>20):          #1번 옷으로 이동함
                num = 1
                count1 = 0
                count2 = 0
                break
            if(count2>20):          #2번 옷으로 이동함
                num = 2
                count1 = 0
                count2 = 0
                break
    
        cv2.destroyAllWindows()

    elif num == 1:      #1번 옷 오버레이 화면
        overlay(num)
        num = 0
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break


    elif num == 2:      #2번 옷 오버레이 화면
        overlay(num)
        num = 0
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
            
cap.release()