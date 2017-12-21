import cv2
import sys
import numpy as np
import cv2
import os


os.system('sudo modprobe bcm2835-v4l2')

#cascPath = sys.argv[0]
bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml') #학습데이터 읽어오기
body_mask = cv2.imread('T-Shirt.png')#이미지 읽어오기
h_mask, w_mask = body_mask.shape[:2] 

if bodyCascade.empty(): 
    raise IOError('Unable to load the mouth cascade classifier xml files')

cap = cv2.VideoCapture(0) #내장 카메라 
scaling_factor = 1.5 #윈도우 크기설정
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
        #x = x-75
        frame_roi = frame[y+150:y+450,x:x+300]
        body_mask_small = cv2.resize(body_mask,(300,300),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 50,255, cv2.THRESH_BINARY_INV)
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

    for (x, y, w, h) in body:
        #cv2.rectangle(frame, (x, y+400), (x+w, y+h+500), (0, 255, 0), 3)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                 break

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
