import cv2
import sys
import numpy as np
import time
import os

cap = cv2.VideoCapture(0)

fist_pattern = cv2.CascadeClassifier('fist.xml')    #학습데이터 읽어오기
scaling_factor = 1.5            #윈도우 크기설정
num = 0                         #화면 전환에 필요한 변수
count1 = 0                      #1번 옷을 선택할때 사용하는 변수
count2 = 0                      #2번 옷을 선택할때 사용하는 변수

T_Shirt1 = 'hoodT1.png'         #흰 티셔츠
T_Shirt2 = 'T-Shirt.png'        #검은 티셔츠

T_Shirt = [T_Shirt1, T_Shirt2]  #티셔츠 배열



def overlay(i):                 #i 번째 옷 오버레이하는 정의 함수
    # clothes - 1 overlay 
    os.system('sudo modprobe bcm2835-v4l2') 
    count = 0                   #오버레이 화면에서 빠져나올때 사용하는 변수

    #cascPath = sys.argv[0]
    bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')    #학습데이터 읽어오기
    body_mask = cv2.imread(T_Shirt[i-1])                                    #T_Shirt배열 i 번째 이미지 읽어오기
    h_mask, w_mask = body_mask.shape[:2] 

    if bodyCascade.empty(): 
        raise IOError('Unable to load the mouth cascade classifier xml files')

    #cap = cv2.VideoCapture(0) #내장 카메라 
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        body = bodyCascade.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minSize=(100,200),
            flags=cv2.CASCADE_SCALE_IMAGE
        )


        # Draw a rectangle around the faces
        for (x, y, w, h) in body:
            x = x-40        
            frame_roi = frame[y+150:y+450,x:x+300]
            body_mask_small = cv2.resize(body_mask,(300,300),interpolation = cv2.INTER_AREA)
            gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)
            if(i==2):
                ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY_INV) # 흰옷이 아닌경우
            elif(i==1):
                ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY) # 흰옷일때 

            mask_inv = cv2.bitwise_not(mask)
            print(body_mask.shape)
            print(body.shape)
            print(x)
            print(y)
            if(x<50 or x>660 or y>270):     #영역 벗어나는거 제외
                continue
            else:
                masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask)
        
                masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        
                frame[y+150:y+450,x:x+300] = cv2.add(masked_body, masked_frame)
                    
                cv2.rectangle(frame, (x, y+150), (x+300 ,y+450), (0, 0, 255), 2)

        for (x, y, w, h) in body:
            #cv2.rectangle(frame, (x, y+400), (x+w, y+h+500), (0, 255, 0), 3)
            if cv2.waitKey(1) and 0xFF == ord('q'):
                break

            

        fistList = fist_pattern.detectMultiScale(gray, 1.5)
        cv2.rectangle(frame, (100, 150), (200, 250), (255, 0, 0), 3)

        for (x, y, w, h) in fistList:       #주먹 인식해서 해당 네모에 있을때 초기화면으로 감 변수명 신경 안써도됨
            if(w>30 and h>25):
                if ((x>450 and y>50) and (x<600 and y<150)) or ((x>50 and y>50) and (x<200 and y<150)): # 주먹이 사각형 범위 안에 있을때만 검출
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

                if((int)((2*x+w)/2)> 100 and (int)((2*x+w)/2) < 200 and (int)((2*y+h)/2) > 150 and (int)((2*y+h)/2) < 250):
                    count = count + 1
                    print (count)
                                 
                    
                    
        cv2.imshow('Video1', frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
            
        if(count>20):
            break
    
    cv2.destroyAllWindows()


#실제 실행 화면 코드
while True:
    if num == 0 :       #초기화면 
        while True:
            ret, frame1 = cap.read()
            frame1 = cv2.resize(frame1,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_AREA)
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            fistList = fist_pattern.detectMultiScale(gray1, 1.5)
            cv2.rectangle(frame1, (450, 50), (600, 150), (255, 0, 0), 3)
            cv2.rectangle(frame1, (50, 50), (200, 150), (255, 0, 0), 3)
            

            for (x, y, w, h) in fistList:
                if(w>30 and h>25):
                    if ((x>450 and y>50) and (x<600 and y<150)) or ((x>50 and y>50) and (x<200 and y<150)): # 주먹이 사각형 범위 안에 있을때만 검출
                        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    #print(x,y,w,h)
                    
                    
                
                    if((int)((2*x+w)/2)> 50 and (int)((2*x+w)/2) < 200 and (int)((2*y+h)/2) > 50 and (int)((2*y+h)/2) < 150):
                        count1 = count1 + 1
                        

                    elif((int)((2*x+w)/2)> 400 and (int)((2*x+w)/2) < 600 and (int)((2*y+h)/2) > 50 and (int)((2*y+h)/2) < 150):
                        count2 = count2 + 1

                    print(count1, count2)
                                 
                    
                    
            cv2.imshow('image', frame1)
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


    elif num == 2:      #2번 옷 오버레이 화면
        overlay(num)
        num = 0


cap.release()
