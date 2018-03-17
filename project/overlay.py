import cv2
import sys
import numpy as np
import time
import os
import Click_Function

prev_x = 0
prev_y = 0
prev_w = 0
prev_h = 0

def masked_Operation(x,y,w,h,img,body_mask,color): # 상체 ROI의 범위를 정하고 이미지를 해당 영역에 덮어씌운다
    
    
    if x>20:                    #어자피 x>20인 경우 실행되는 함수이므로 불필요 한듯
        x = x-10
    else:
        pass
    y_offset = 130        # 이미지 사이즈 조정
    img_size = 260

    

    frame_roi = img[y+y_offset:y+y_offset+img_size, x:x+img_size]
    
    cv2.imshow('video2',frame_roi)              # 그냥 상체 오버레이 영역 보여줌
    
    body_mask_small = cv2.resize(body_mask,(img_size,img_size),interpolation = cv2.INTER_CUBIC) # 옷이미지 키우기? 정하기
    gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)# 키운 이미지의 gray처리 (BGR->Gray)
    
    
    if(color==2):
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY_INV) # 흰옷이 아닌경우
            
    elif(color==1):
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY) # 흰옷일때

    mask_inv = cv2.bitwise_not(mask)
    try:       
        masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask) # 오버레이되는 부분만 남게된다.
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv) #배경만 남게된다
        img[y+y_offset:y+y_offset+img_size, x:x+img_size] = cv2.add(masked_body, masked_frame) # 화면에 이미지 오버레이
    except:
        print('Error')   # 에러 발생할때 이미지 오버레이를 전 오버레이를 적용할 수 있으면 좀 더 자연스러워 질 듯
     
def Range_Operation(body,img,body_mask,color):    # 예외범위를 추가한 코드
    count = 0
    global prev_x
    global prev_y
    global prev_w
    global prev_h
    
    for (x, y, w, h) in body:
        

        if (abs(prev_x-x) < 10) and (abs(prev_y-y) < 10): #이전 x,y 와 현재 x,y의 차이가 별로 나지 않으면 이전 위치의 이미지 출력
            print('small')
            continue
        
        if (prev_w != 0):             
            if (abs(prev_w-w) > 20) and (abs(prev_h-h) > 20):
                continue
        
        count = count + 1
        if(count >= 2):
            break
        
        
        
        if  (x>0 and x<540):     # 특정 영역을 벗어나지 않으면 오버레이
            print('now')
            masked_Operation(x,y,w,h,img,body_mask,color)

        else:          
            continue

        prev_x = x
        prev_y = y
        prev_w = w
        prev_h = h
            
    if (count == 0):   # 이동 전, 후 차이가 적으면 이전 오버레이위치 출력 
        if (prev_x !=0 and prev_y !=0 and prev_w != 0 and prev_h !=0):
            print('pre')
            masked_Operation(prev_x,prev_y,prev_w,prev_h,img,body_mask,color)
 
        
def Full_Overlay(cap,imag,color):       #이전에 정의했던 함수들을 모아서 처리

    bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')    #학습데이터 읽어오기
    

    TextPosition1= (540,110)
    TextPosition2= (540,250)
    TextPosition3= (540,390)
    
    body_mask = cv2.imread(imag)  #애니메이션으로 부터  이미지 읽어오기
    

    if bodyCascade.empty(): #학습데이터 없을시 에러메세지
        raise IOError('Unable to load the mouth cascade classifier xml files')

    while True:
        ret, frame = cap.read()
        img = cv2.flip(frame,1)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # BGR-> Gray
      
        body = bodyCascade.detectMultiScale(
            gray,
            minSize=(100,200),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        Click_Function.draw_Click(img,TextPosition1,(500,70),(620,140),'Reco')
        Click_Function.draw_Click(img,TextPosition2,(500,210),(620,280),'List')
        Click_Function.draw_Click(img,TextPosition3,(500,350),(620,420),'Buy')

        
        Range_Operation(body,img,body_mask,color)
    
                                   
        cv2.imshow('video', img)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()

cap = cv2.VideoCapture(0)
color= 1
Full_Overlay(cap,"hoodT1_White.png",color)
