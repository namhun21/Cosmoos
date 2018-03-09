import cv2
import numpy as np

def animationleft(firstindex,secondindex,thirdindex,fourthindex,move,frame):
    clothes0 = 'coat.png'
    clothes1 = 'hoodT1.png'
    clothes2 = 'T-shirt.png'
    clothes3 = 'pants1.png'
    clothes4 = 'super.png'
    clothes = [clothes0,clothes1,clothes2,clothes3,clothes4]
    maskclo = cv2.imread(clothes[firstindex])
    mask_small = cv2.resize(maskclo,(100-11*move, 100-11*move),interpolation = cv2.INTER_AREA)
    gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_roi = frame[30-3*move:30-3*move+100-11*move,50-5*move:50-5*move+100-11*move]
    masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
    frame[30-3*move:30-3*move+100-11*move,50-5*move:50-5*move+100-11*move] = cv2.add(masked_body, masked_frame)
    maskclo = cv2.imread(clothes[secondindex])
    mask_small = cv2.resize(maskclo,(150-5-5*move,125-7-2*move),interpolation = cv2.INTER_AREA)
    gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_roi = frame[75-5*move:75-5*move+125-7-2*move,250-20-20*move:250-20-20*move+150-5-5*move]
    masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
    frame[75-5*move:75-5*move+125-7-2*move,250-20-20*move:250-20-20*move+150-5-5*move] = cv2.add(masked_body, masked_frame)
    maskclo = cv2.imread(clothes[thirdindex])
    mask_small = cv2.resize(maskclo,(100+5+5*move,100+7+2*move),interpolation = cv2.INTER_AREA)
    gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_roi = frame[30+5*move:30+5*move+100+7+2*move,480-23-23*move:480-23-23*move+100+5+5*move]
    masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
    frame[30+5*move:30+5*move+100+7+2*move,480-23-23*move:480-23-23*move+100+5+5*move] = cv2.add(masked_body, masked_frame)
    maskclo = cv2.imread(clothes[fourthindex])
    mask_small = cv2.resize(maskclo,(10+10*move,10+10*move),interpolation = cv2.INTER_AREA)
    gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_roi = frame[3+3*move:3+3*move+10+10*move,590-11-11*move:590-11-11*move+10+10*move]
    masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
    frame[3+3*move:3+3*move+10+10*move,590-11-11*move:590-11-11*move+10+10*move] = cv2.add(masked_body, masked_frame)
