import cv2
import numpy as np


def clicka():
    cap = cv2.VideoCapture(0)


    count =0
    num = 0
    time = 0
    touch = 0
    check = 0
    kernel = np.ones((5,5),np.uint8)

    while(cap.isOpened()):
        ret, img = cap.read()
        img1 = img.copy()
    ##    cv2.imshow('input',img)
        roi = img1[b:d,a:c]
        cv2.rectangle(img,(a,b),(c,d),(255,0,0),3)
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        roigray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    ##    ret, immaskori = cv2.threshold(imgray,180,0,cv2.THRESH_BINARY)


        if(check == 0 and time > 100):
            cap1 = cv2.VideoCapture(0)
            ret, ori2 = cap1.read()
            oriroi = ori2[b:d,a:c]
            origray = cv2.cvtColor(ori2,cv2.COLOR_BGR2GRAY)
            origraysc = origray[b:d,a:c]
            cv2.imshow('asdasdasdaq',origray)
            check = 1


        if(check == 1):
            for x in range(c-a):
                for y in range(d-b):
                  oricolor = roigray[y,x]
                  roicolor = origraysc[y,x]
                  if(oricolor- roicolor < 30):
                       roi[y,x] = 0
                  else:
                       roi[y,x] = 255
                       num = num+1

        print(num)
        if(num > 15000 * 0.5 and count == 0 and time > 50):
            count = 0
            touch = 0
            print("success")

        num = 0
        print(count)
    ##    erosion = cv2.erode(roi,kernel,iterations= 1)
    ##    opening = cv2.morphologyEx(roi,cv2.MORPH_OPEN,kernel)
        cv2.imshow('gray',imgray)
    ##    cv2.imshow('asd',opening)
        cv2.imshow('sads',roigray)
        time  = time + 1
        k = cv2.waitKey(10)
        if k==27:
            break

    cv2.destroyAllWindows()

clicka(0,0,150,100)

