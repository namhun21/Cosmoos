import cv2
import numpy as np


mouth_cascade =  cv2.CascadeClassifier('Mouth.xml')
moustache_mask = cv2.imread('moustache.png')
h_mask, w_mask = moustache_mask.shape[:2]

if mouth_cascade.empty():
    raise IOError('Unable to load the  mouth cascade classifier xml files')

cap = cv2.VideoCapture(0)
scaling_factor = 0.9

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    mouth_rects = mouth_cascade.detectMultiScale(gray,1.3,5)
    if len(mouth_rects) > 0:
        (x,y,w,h) = mouth_rects[0]
        h,w = int(50), int(70)
        x = x - int(0.05*w)
        y = y - int(0.55*h)
        frame_roi = frame[y:y+50,x:x+70]
        moustache_mask_small = cv2.resize(moustache_mask,(w,h),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(moustache_mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 50,255, cv2.THRESH_BINARY_INV)
        mask_inv = cv2.bitwise_not(mask)
        print(moustache_mask.shape)
        print(mask.shape)
        masked_mouth = cv2.bitwise_and(moustache_mask_small,moustache_mask_small, mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask=mask_inv)
        frame[y:y+h,x:x+w] = cv2.add(masked_mouth, masked_frame)
        
    cv2.imshow('Moustache',frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
