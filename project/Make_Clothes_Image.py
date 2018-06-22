import cv2
import numpy as np

#김남훈 학생이 기초를 만들고 정재진 학생이 이를 도와 코드를 완성하였습니다.
#코드 구조화 과정의 일환입니다.

def make_Clothes_Image(clothes,size,y1,y2,x1,x2,frame):
    maskclo = cv2.imread('./image/'+clothes)
    mask_small = cv2.resize(maskclo,size,interpolation = cv2.INTER_AREA)
    gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
    # color = clothes.split("_")[1]
    ret, mask = cv2.threshold(gray_mask, 248,255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    frame_roi = frame[y1:y2,x1:x2]
    masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
    frame[y1:y2,x1:x2] = cv2.add(masked_body, masked_frame)


def make_Button_Image(button,size,y1,y2,x1,x2,frame):
    maskclo = cv2.imread('./image/'+button)
    mask_small = cv2.resize(maskclo,size,interpolation = cv2.INTER_AREA)
    gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
    # color = clothes.split("_")[1]
    ret, mask = cv2.threshold(gray_mask, 10,255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_roi = frame[y1:y2,x1:x2]
    masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
    frame[y1:y2,x1:x2] = cv2.add(masked_body, masked_frame)

def make_Button_Image_Black(button,size,y1,y2,x1,x2,frame):
    maskclo = cv2.imread('./image/'+button)
    mask_small = cv2.resize(maskclo,size,interpolation = cv2.INTER_AREA)
    gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
    # color = clothes.split("_")[1]
    ret, mask = cv2.threshold(gray_mask, 248,255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    frame_roi = frame[y1:y2,x1:x2]
    masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
    masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
    frame[y1:y2,x1:x2] = cv2.add(masked_body, masked_frame)
