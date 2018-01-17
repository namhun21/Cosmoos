import cv2
import sys
import numpy as np
import os


os.system('sudo modprobe bcm2835-v4l2')

#cascPath = sys.argv[0]
bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml') #학습데이터 읽어오기
fist_pattern = cv2.CascadeClassifier('fist.xml')
T_Shirt1 = 'T-Shirt.png'
T_Shirt2 = 'T-Shirt2.png'
T_Shirt3 = 'T-Shirt3.png'
T_Shirt = [T_Shirt1, T_Shirt2, T_Shirt3]
number = 0 # T-Shirt 배열 인덱스

def Intro(i):
    cap = cv2.VideoCapture(0) #내장 카메라 
    scaling_factor = 1.5 #윈도우 크기설정
    count = 0
    i = 0
    while True:
        body_mask = cv2.imread(T_Shirt[i])#이미지 읽어오기
        h_mask, w_mask = body_mask.shape[:2]

        if bodyCascade.empty(): 
            raise IOError('Unable to load the mouth cascade classifier xml files')
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
        fistList = fist_pattern.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
            )
        cv2.rectangle(frame, (450, 50), (600, 150), (255, 0, 0), 3)
        cv2.rectangle(frame, (50, 50), (200, 150), (255, 0, 0), 3)

        for (x, y, w, h) in fistList:           
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            if ((int)((2 * x + w) / 2) > 50 and (int)((2 * x + w) / 2) < 200 and (int)((2 * y + h) / 2) > 50 and (int)((2 * y + h) / 2) < 150):
                count = count + 1
                print (count)
                if(count>20):
                    i = i+1
                    count = 0
            elif ((int)((2 * x + w) / 2) > 400 and (int)((2 * x + w) / 2) < 600 and (int)((2 * y + h) / 2) > 50 and (int)((2 * y + h) / 2) < 150):
                count = count - 1
                print (count)
                if(count<-20):
                    i = i-1
                    count = 0
                    
        # Draw a rectangle around the faces
        for (x, y, w, h) in body:
            x = x-75
            frame_roi = frame[y+150:y+450,x:x+300]
            body_mask_small = cv2.resize(body_mask,(300,300),interpolation = cv2.INTER_AREA)
            gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)
            if(i==0 or i== -3):
                ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY_INV)
            elif(i==1 or i== -2):
                ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
            elif(i==2 or i== -1):
                ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY_INV)
            mask_inv = cv2.bitwise_not(mask)
            print(body_mask.shape)
            print(body.shape)
            print(x)
            print(y)
            if(x<50 or x>660 or y>270):
                continue
            else:
                masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask)
        
                masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask=mask_inv)
        
                frame[y+150:y+450,x:x+300] = cv2.add(masked_body, masked_frame)
        
                cv2.rectangle(frame, (x, y+150), (x+300 ,y+450), (0, 255, 0), 2)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

Intro(number)
