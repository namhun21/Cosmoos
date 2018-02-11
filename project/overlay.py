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

def masked_Operation(x,y,w,h,frame,body_mask):
    x = x-40        
    img_size = w + 50
    y_offset = 220

    frame_roi = frame[y+y_offset:y+y_offset+img_size, x:x+img_size]
    body_mask_small = cv2.resize(body_mask,(img_size,img_size),interpolation = cv2.INTER_AREA) # 옷이미지 키우기
    gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)#키운 이미지에 대한 mask (BGR->Gray)
    #if(i==2):
     #   ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY_INV) # 흰옷이 아닌경우
            
    #elif(i==1):
    ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY) # 흰옷일때

    mask_inv = cv2.bitwise_not(mask)
         

    if(x<100 or x>550 or y>200):     #영역 벗어나는거 제외
        pass
    else:
        masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask) # 오버레이되는 부분만 남게된다.
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv) #배경만 남게된다
        frame[y+y_offset:y+y_offset+img_size, x:x+img_size] = cv2.add(masked_body, masked_frame) # 화면에 이미지 오버레이
    
prev_x = 0
prev_y = 0
prev_w = 0
prev_h = 0

def Operation(body,frame,body_mask):
    count = 0
    global prev_x
    global prev_y
    global prev_w
    global prev_h
    
    for (x, y, w, h) in body:
        
        print('x = ',x,'y = ',y,'w = ',w,'h = ',h)

        if (abs(prev_x-x) < 10) and (abs(prev_y-y) < 10): #이전 x,y 와 현재 x,y의 차이가 별로 나지 않으면 
            print('prev_x =', prev_x, 'x = ', x, 'prev_y = ',prev_y, 'y = ', y, 'w= ',prev_w, 'h = ',prev_h)
            continue

        if (prev_w != 0):
            if (abs(prev_w-w) > 10) and (abs(prev_h-h) > 10):
                print('prev_w = ',prev_w,'w = ',w,'prev_h = ',prev_h,'h = ',h)
                continue
        
        count = count + 1
        if(count >= 2):
            break

        prev_x = x
        prev_y = y
        prev_w = w
        prev_h = h

        masked_Operation(x,y,w,h,frame,body_mask)
        
            
    if (count == 0):
        if (prev_x !=0 and prev_y !=0 and prev_w != 0 and prev_h !=0):
            masked_Operation(prev_x,prev_y,prev_w,prev_h,frame,body_mask)
            
        #cv2.rectangle(frame,(prev_x,prev_y),(prev_x+prev_w,prev_y+prev_h),(0,255,255),2)
        #draw_shirt(x,y,w,h)
        
            
def Full_Overlay():       #i 번째 옷 오버레이하는 정의 함수
    # clothes - 1 overlay 
    os.system('sudo modprobe bcm2835-v4l2') 

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

        # Draw a rectangle around the faces
        Operation(body,frame,body_mask)
    

                                     
        cv2.imshow('Video1', frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    

def running():
#실제 실행 화면 코드
    global num
    global count1
    global count2
    while True:
        if num == 0:      #1번 옷 오버레이 화면
            Full_Overlay()
            num = 0
            if cv2.waitKey(1) and 0xFF == ord('q'):
                break

        elif num == 1:      #2번 옷 오버레이 화면
            Full_Overlay()
            num = 0
            if cv2.waitKey(1) and 0xFF == ord('q'):
                break

        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
            
    cap.release()

num = 0                         #화면 전환에 필요한 변수
count1 = 0                      #1번 옷을 선택할때 사용하는 변수
count2 = 0                      #2번 옷을 선택할때 사용하는 변수

cap = cv2.VideoCapture(0)
fist_pattern = cv2.CascadeClassifier('fist.xml')    #학습데이터 읽어오기
bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')    #학습데이터 읽어오기
scaling_factor = 1.5            #윈도우 크기설정



