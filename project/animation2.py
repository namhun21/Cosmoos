import cv2
import numpy as np
cap = cv2.VideoCapture(0)
count = 0
countl = 0
countr = 0
timel = 0
timer = 0
touchl = 0
touchr = 0
check = 0
kernerl = np.ones((5,5),np.uint8)
time = 0
stop = 0
stoper = 0
numl = 0
numr = 0

while(cap.isOpened()):
    ret, img = cap.read()
    img1 = img.copy()
    roil = img1[400:500,0:150]
    roir = img1[400:500,500:650]
    cv2.rectangle(img,(0,400),(150,500),(255,0,0),3)
    cv2.rectangle(img,(500,400),(650,500),(255,0,0),3)
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    roil = cv2.cvtColor(roil,cv2.COLOR_BGR2GRAY)
    grayroir = cv2.cvtColor(roir,cv2.COLOR_BGR2GRAY)

    if(check == 0 and timer > 100):
        cap1 = cv2.VideoCapture(0)
        ret,ori = cap1.read()
        oriroil = ori[400:500,0:150]
        oriroir = ori[400:500,500:650]

        origrayl = cv2.cvtColor(oriroil,cv2.COLOR_BGR2GRAY)
        origrayr = cv2.cvtColor(oriroir,cv2.COLOR_BGR2GRAY)

##        cv2.imshow('qhsjdhsjka',origrayl)
        check = 1


    if(check == 1):
##        for x in range(150):
##            for y in range(100):
##              oricolorl = roigray[y,x]
##              roicolorl = origraylsc[y,x]
##              if(oricolor- roicolor < 30):
##                   roi[y,x] = 0
##              else:
##                   roi[y,x] = 255
##                   numl = numl+1
        for x in range(150):
            for y in range(100):
              oricolor = origrayr[y,x]
              roicolor = grayroir[y,x]
              if(oricolor- roicolor < 30):
                   roir[y,x] = 0
              else:
                   roir[y,x] = 255
                   numr = numr+1


    if(numl > 15000 * 0.07 and countl == 0 and timel > 50 and touchl < 30):
        countl = 1
    if(countl == 1 and numl < 15000 * 0.1 and touchl < 30):
        countl = 2
    if(countl == 2 and numl > 15000 * 0.15 and touchl < 30):
        countl = 3
    if(countl ==3 and numl < 15000* 0.1 and touch < 30):
        countl = 0
        if(count == 4):
            count = 0
        else:
            count = count +1
    touchl = touchl + 1
    if(touchl == 31):
        touchl = 0
        countl = 0

    if(numr > 15000 * 0.07 and countr == 0 and timer > 50 and touchr < 30):
        countr = 1
    if(countr== 1 and numr < 15000 * 0.1 and touchr < 30):
        countr = 2
    if(countr == 2 and numr > 15000 * 0.15 and touchr < 30):
        countr = 3
    if(countr ==3 and numr < 15000* 0.1 and touchr < 30):
        countr = 0
        stop = 1
    touchr = touchr + 1
    if(touchr == 31):
        touchr = 0
        countr = 0
    clothes0 = 'coat.png'
    clothes1 = 'hoodT1.png'
    clothes2 = 'T-shirt.png'
    clothes3 = 'pants1.png'
    clothes4 = 'super.png'

    if(stop == 1):
        time  = time + 1

    clothes = [clothes0,clothes1,clothes2,clothes3,clothes4]
    print(count)
    if(count == 0):
        maskclo = cv2.imread(clothes[count +3])
        mask_small = cv2.resize(maskclo,(10+10*time, 10+10*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[3+3*time:3+3*time+10+10*time,5+5*time:5+5*time+10+10*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[3+3*time:3+3*time+10+10*time,5+5*time:5+5*time+10+10*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count+4])
        mask_small = cv2.resize(maskclo,(100+5+5*time,100+7+2*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[30+5*time:30+5*time+100+7+2*time,50+20+20*time:50+20+20*time+100+5+5*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[30+5*time:30+5*time+100+7+2*time,50+20+20*time:50+20+20*time+100+5+5*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count])
        mask_small = cv2.resize(maskclo,(150-5*time,125-7-2*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[75-5*time:75-5*time+125-7-2*time,250+23+23*time:250+23+23*time + 150-5*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[75-5*time:75-5*time+125-7-2*time,250+23+23*time:250+23+23*time + 150-5*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count + 1])
        mask_small = cv2.resize(maskclo,(100-11*time,100-11*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[30-3*time:30-3*time+100-11*time,480+12+12*time:480+12+12*time+100-11*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[30-3*time:30-3*time+100-11*time,480+12+12*time:480+12+12*time+100-11*time] = cv2.add(masked_body, masked_frame)

    elif(count == 4):
        maskclo = cv2.imread(clothes[count -2])
        mask_small = cv2.resize(maskclo,(10+10*time, 10+10*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[3+3*time:3+3*time+10+10*time,5+5*time:5+5*time+10+10*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[3+3*time:3+3*time+10+10*time,5+5*time:5+5*time+10+10*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count-1])
        mask_small = cv2.resize(maskclo,(100+5+5*time,100+7+2*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[30+5*time:30+5*time+100+7+2*time,50+20+20*time:50+20+20*time+100+5+5*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[30+5*time:30+5*time+100+7+2*time,50+20+20*time:50+20+20*time+100+5+5*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count])
        mask_small = cv2.resize(maskclo,(150-5*time,125-7-2*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[75-5*time:75-5*time+125-7-2*time,250+23+23*time:250+23+23*time + 150-5*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[75-5*time:75-5*time+125-7-2*time,250+23+23*time:250+23+23*time + 150-5*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count -4])
        mask_small = cv2.resize(maskclo,(100-11*time,100-11*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[30-3*time:30-3*time+100-11*time,480+12+12*time:480+12+12*time+100-11*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[30-3*time:30-3*time+100-11*time,480+12+12*time:480+12+12*time+100-11*time] = cv2.add(masked_body, masked_frame)

    elif(count == 1):
        maskclo = cv2.imread(clothes[count +3])
        mask_small = cv2.resize(maskclo,(10+10*time, 10+10*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[3+3*time:3+3*time+10+10*time,5+5*time:5+5*time+10+10*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[3+3*time:3+3*time+10+10*time,5+5*time:5+5*time+10+10*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count-1])
        mask_small = cv2.resize(maskclo,(100+5+5*time,100+7+2*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[30+5*time:30+5*time+100+7+2*time,50+20+20*time:50+20+20*time+100+5+5*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[30+5*time:30+5*time+100+7+2*time,50+20+20*time:50+20+20*time+100+5+5*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count])
        mask_small = cv2.resize(maskclo,(150-5*time,125-7-2*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[75-5*time:75-5*time+125-7-2*time,250+23+23*time:250+23+23*time + 150-5*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[75-5*time:75-5*time+125-7-2*time,250+23+23*time:250+23+23*time + 150-5*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count +1])
        mask_small = cv2.resize(maskclo,(100-11*time,100-11*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[30-3*time:30-3*time+100-11*time,480+12+12*time:480+12+12*time+100-11*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[30-3*time:30-3*time+100-11*time,480+12+12*time:480+12+12*time+100-11*time] = cv2.add(masked_body, masked_frame)
    else:
        maskclo = cv2.imread(clothes[count -2])
        mask_small = cv2.resize(maskclo,(10+10*time, 10+10*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[3+3*time:3+3*time+10+10*time,5+5*time:5+5*time+10+10*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[3+3*time:3+3*time+10+10*time,5+5*time:5+5*time+10+10*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count-1])
        mask_small = cv2.resize(maskclo,(100+5+5*time,100+7+2*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[30+5*time:30+5*time+100+7+2*time,50+20+20*time:50+20+20*time+100+5+5*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[30+5*time:30+5*time+100+7+2*time,50+20+20*time:50+20+20*time+100+5+5*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count])
        mask_small = cv2.resize(maskclo,(150-5*time,125-7-2*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[75-5*time:75-5*time+125-7-2*time,250+23+23*time:250+23+23*time + 150-5*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[75-5*time:75-5*time+125-7-2*time,250+23+23*time:250+23+23*time + 150-5*time] = cv2.add(masked_body, masked_frame)
        maskclo = cv2.imread(clothes[count + 1])
        mask_small = cv2.resize(maskclo,(100-11*time,100-11*time),interpolation = cv2.INTER_AREA)
        gray_mask = cv2.cvtColor(mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 127,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_roi = img[30-3*time:30-3*time+100-11*time,480+12+12*time:480+12+12*time+100-11*time]
        masked_body = cv2.bitwise_and(mask_small,mask_small,mask = mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv)
        img[30-3*time:30-3*time+100-11*time,480+12+12*time:480+12+12*time+100-11*time] = cv2.add(masked_body, masked_frame)

    if(time == 9):
        if(count == 0):
            count = 4
            stop = 0

        else:
            count = count -1
        time = 0

    timer = timer + 1
##    if(count == 0):
##        mask1 =
##    cv2.rectangle(img,(450,0),(600,130),(0,255,0),3)
##    cv2.rectangle(img,(450,130),(600,330),(0,255,0),3)
##    cv2.rectangle(img,(450,330),(600,460),(0,255,0),3)

##    cv2.imshow('aasd',img)
##    cv2.imshow('asd',frame_roi)
    cv2.imshow('wqzxcq',grayroir)
    cv2.imshow('asdasda',img)

    k = cv2.waitKey(10)
    if k==27:
        break

cv2.destroyAllWindows()