import cv2
import numpy as np


def clicka():
    cap = cv2.VideoCapture(0)


    num1 = 0
    num2 = 0
    num3 = 0
    count1 = 0
    count2 = 0
    count3 = 0

    time = 0
    check = 0
    kernel = np.ones((5,5),np.uint8)

    while(cap.isOpened()):
        ret, img = cap.read()
        img1 = img.copy()
    ##    cv2.imshow('input',img)
        roi1 = img1[50:80,450:570]
        roi2 = img1[50:80,250:370]
        roi3 = img1[50:80,50:170]

        cv2.rectangle(img,(450,50),(570, 80),(255,0,0),3)
        cv2.rectangle(img,(250,50),(370,80),(255,0,0),3)
        cv2.rectangle(img,(50,50),(170,80),(255,0,0),3)

        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        roigray1 = cv2.cvtColor(roi1,cv2.COLOR_BGR2GRAY)
        roigray2 = cv2.cvtColor(roi2,cv2.COLOR_BGR2GRAY)
        roigray3 = cv2.cvtColor(roi3,cv2.COLOR_BGR2GRAY)

    ##    ret, immaskori = cv2.threshold(imgray,180,0,cv2.THRESH_BINARY)


        if(check == 0 and time > 100):
            cap1 = cv2.VideoCapture(0)
            ret, ori2 = cap1.read()
            
            oriroi1 = ori2[50:80,450:570]
            oriroi2 = ori2[50:80,250:370]
            oriroi3 = ori2[50:80,50:170]

            origray = cv2.cvtColor(ori2,cv2.COLOR_BGR2GRAY)
            
            origraysc1 = origray[50:80,450:570]
            origraysc2 = origray[50:80,250:370]
            origraysc3 = origray[50:80,50:170]

            #cv2.imshow('asdasdasdaq',origray)
            check = 1


        if(check == 1):
            for x in range(120):
                for y in range(30):
                  oricolor1 = roigray1[y,x]
                  roicolor1 = origraysc1[y,x]
                  oricolor2 = roigray2[y,x]
                  roicolor2 = origraysc2[y,x]
                  oricolor3 = roigray3[y,x]
                  roicolor3 = origraysc3[y,x]
                  if(oricolor1- roicolor1 < 30):
                       roi1[y,x] = 0
                  else:
                       roi1[y,x] = 255
                       num1 = num1+1
                  if(oricolor2- roicolor2 < 30):
                       roi2[y,x] = 0
                  else:
                       roi2[y,x] = 255
                       num2 = num2+1
                  if(oricolor3- roicolor3 < 30):
                       roi3[y,x] = 0
                  else:
                       roi3[y,x] = 255
                       num3 = num3+1

       # print(num1,num2,num3)
        

        if(num1 > 3600 * 0.5  and time > 50):

            count1 = count1+1

        num1 = 0

        if(num2 > 3600 * 0.5  and time > 50):

            count2 = count2+1


        num2 = 0

        if(num3 > 3600 * 0.5  and time > 50):

            count3 = count3+1
            

        num3 = 0

        print(count1, count2, count3)

        if(count1 > 30):
            print("success1")
            count1 = 0
            count2 = 0
            count3 = 0
        elif(count2 > 30):
            print("success2")
            count1 = 0
            count2 = 0
            count3 = 0
        elif(count3 > 30):
            print("success3")
            count1 = 0
            count2 = 0
            count3 = 0

        


        
    ##    erosion = cv2.erode(roi,kernel,iterations= 1)
    ##    opening = cv2.morphologyEx(roi,cv2.MORPH_OPEN,kernel)
        cv2.imshow('gray',imgray)
    ##    cv2.imshow('asd',opening)
        cv2.imshow('sads1',roigray1)
        cv2.imshow('sads2',roigray2)
        cv2.imshow('sads3',roigray3)

        time  = time + 1
        k = cv2.waitKey(10)
        if k==27:
            break

    cv2.destroyAllWindows()

clicka()
