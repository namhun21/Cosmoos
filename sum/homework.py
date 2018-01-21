import cv2
import sys
import numpy as np
import time
import os


def Read_TS(): 
    T_Shirt1 = 'hoodT1.png'         #흰 티셔츠
    T_Shirt2 = 'T-Shirt.png'        #검은 티셔츠
    T_Shirt = [T_Shirt1, T_Shirt2]  #티셔츠 배열
    return T_Shirt


def overlay(i):                 #i 번째 옷 오버레이하는 정의 함수
    # clothes - 1 overlay 
    os.system('sudo modprobe bcm2835-v4l2') 
    count = 0                   #오버레이 화면에서 빠져나올때 사용하는 변수

    T_Shirt=Read_TS()
    body_mask = cv2.imread(T_Shirt[i-1])                                    #T_Shirt배열 i 번째 이미지 읽어오기
    h_mask, w_mask = body_mask.shape[:2] #이미지 영역

    if bodyCascade.empty(): #학습데이터 없을시 에러메세지
        raise IOError('Unable to load the mouth cascade classifier xml files')

    while True:
        # Capture frame-by-frame
        frame,body,gray=Capture_Frame()
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
    
def Capture_Frame():
    ret, frame = cap.read() # 비디오 설정
    frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # BGR-> Gray

    body = bodyCascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minSize=(100,200),
        flags=cv2.CASCADE_SCALE_IMAGE
        )
    return frame, body, gray

def Operation(body,frame,body_mask,i):
    for (x, y, w, h) in body:
        x = x-40        
        frame_roi = frame[y+150:y+450,x:x+300]
        body_mask_small = cv2.resize(body_mask,(300,300),interpolation = cv2.INTER_AREA) # 옷이미지 키우기
        cv2.imshow('imag',body_mask_small)
        gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)#키운 이미지에 대한 mask (BGR->Gray)
        cv2.imshow('gray_mask',gray_mask)
        if(i==2):
            ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY_INV) # 흰옷이 아닌경우
            cv2.imshow('mask',mask)
            
        elif(i==1):
            ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY) # 흰옷일때
            cv2.imshow('mask',mask)

        mask_inv = cv2.bitwise_not(mask)

        if(x<50 or x>660 or y>270):     #영역 벗어나는거 제외
            continue
        else:
            masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask) # 오버레이되는 부분만 남게된다.
            
            masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv) #배경만 남게된다
            cv2.imshow('m_f',masked_frame)
            frame[y+150:y+450,x:x+300] = cv2.add(masked_body, masked_frame) # 화면에 이미지 오버레이
            cv2.rectangle(frame, (x, y+150), (x+300 ,y+450), (0, 0, 255), 2)
            

 
def draw_Fist(x,y,w,h,frame,count):
    if(w>30 and h>25):
        if ((x>450 and y>50) and (x<600 and y<150)) or ((x>50 and y>50) and (x<200 and y<150)): # 주먹이 사각형 범위 안에 있을때만 검출
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        if((int)((2*x+w)/2)> 100 and (int)((2*x+w)/2) < 200 and (int)((2*y+h)/2) > 150 and (int)((2*y+h)/2) < 250):
            count = count + 1
            
def Show_Button():
    ret, frame1 = cap.read()
    frame1 = cv2.resize(frame1,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_AREA)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    fistList = fist_pattern.detectMultiScale(gray1, 1.5)
    cv2.rectangle(frame1, (450, 50), (600, 150), (255, 0, 0), 3)
    cv2.rectangle(frame1, (50, 50), (200, 150), (255, 0, 0), 3)
    return frame1,fistList

def CountNum(x,y,w,h,frame1):
    global count1
    global count2
    if(w>30 and h>25):
        if ((x>450 and y>50) and (x<600 and y<150)) or ((x>50 and y>50) and (x<200 and y<150)): # 주먹이 사각형 범위 안에 있을때만 검출
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 3)
                   
                
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
