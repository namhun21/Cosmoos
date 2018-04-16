import cv2
import numpy as np
import time


def make_Clothes_Image(clothes,size,y1,y2,x1,x2,frame):
    millis_start = int(round(time.time() * 1000))
    maskclo = cv2.imread(clothes)
    mask_small = cv2.resize(maskclo,size,interpolation = cv2.INTER_AREA)
    gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
    color = clothes.split("_")[1]
##    if((color == "black") or (color == "blue") or (color == "red")):
    ret, mask = cv2.threshold(gray_mask, 240,255, cv2.THRESH_BINARY_INV)
##    else:
##        ret, mask = cv2.threshold(gray_mask, ,255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_roi = frame[y1:y2,x1:x2]
    masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
    frame[y1:y2,x1:x2] = cv2.add(masked_body, masked_frame)
    millis_end = int(round(time.time() * 1000))
    print("make_Clothes_Image : ",millis_end - millis_start,"ms")
