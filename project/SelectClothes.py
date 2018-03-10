import cv2
import numpy as np
import AnimationRightCall
import AnimationLeftCall
import overlay

def SelectClothes():

    cap = cv2.VideoCapture(0)
    index = 0
    leftcount = 0
    rightcount = 0
    overlaycount = 0
    LeftOn = 0
    RightOn = 0
    startcompare = 0
    animationUnit = 0
    timeright = 0
    timeLeft = 0
    move = 0
    whiteNumLeft = 0
    whiteNumRight = 0
    whiteNumOverlay = 0

    while(cap.isOpened()):
        ret, img = cap.read()
        img1 = img.copy()

        cv2.rectangle(img,(0,350),(150,450),(255,0,0),3)
        cv2.rectangle(img,(450,350),(600,450),(255,0,0),3)
        cv2.rectangle(img,(450,200),(600,300),(255,0,0),3)
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        leftButtonFrame = imgray[350:450,0:150]
        rightButtonFrame = imgray[350:450,450:600]
        overlayButtonFrame = imgray[200:300,450:600]

        if(startcompare == 0 and timeright > 100 and timeLeft > 100):
            picturegray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            pictureleftButtonFrame = picturegray[350:450,0:150]
            picturerightButtonFrame = picturegray[350:450,450:600]
            pictureoverlayButtonFrame = picturegray[200:300,450:600]
            startcompare = 1

        if(startcompare == 1):
            for x in range(150):
                for y in range(100):
                  picturecolor = rightButtonFrame[y,x]
                  rightButtonFrameColor = picturerightButtonFrame[y,x]
                  if(picturecolor- rightButtonFrameColor < 30):
                       rightButtonFrame[y,x] = 0
                  else:
                       rightButtonFrame[y,x] = 255
                       whiteNumRight = whiteNumRight+1

            for x in range(150):
                for y in range(100):
                  picturecolor = leftButtonFrame[y,x]
                  leftButtonFrameColor = pictureleftButtonFrame[y,x]
                  if(picturecolor - leftButtonFrameColor < 30):
                       leftButtonFrame[y,x] = 0
                  else:
                       leftButtonFrame[y,x] = 255
                       whiteNumLeft = whiteNumLeft+1


            for x in range(150):
                for y in range(100):
                  picturecolor = overlayButtonFrame[y,x]
                  overlayButtonColor = pictureoverlayButtonFrame[y,x]
                  if(picturecolor- overlayButtonColor < 30):
                       overlayButtonFrame[y,x] = 0
                  else:
                       overlayButtonFrame[y,x] = 255
                       whiteNumOverlay = whiteNumOverlay+1

        if(rightcount ==0 and whiteNumRight > 15000*0.8):
            LeftOn = 0
            RightOn = 1
            move = 1



        if(leftcount ==0 and whiteNumLeft > 15000*0.8):
            LeftOn = 1
            RightOn = 0
            move = 1


        if(overlaycount == 0 and whiteNumOverlay > 15000*0.8):
            overlay.Full_Overlay()


        if(move == 1):
            animationUnit = animationUnit + 1

        if(index == 0):
            if(RightOn == 1):
                  AnimationRightCall.animationright(index+3,index+4,index,index+1,animationUnit,img)
            else:
                AnimationLeftCall.animationleft(index+4,index,index+1,index+2,animationUnit,img)
        elif(index == 4):
            if(RightOn == 1):
                AnimationRightCall.animationright(index-2,index-1,index,index-4,animationUnit,img)
            else:
                AnimationLeftCall.animationleft(index-1,index,index-4,index-3,animationUnit,img)
        elif(index == 1 and RightOn == 1):
            AnimationRightCall.animationright(index+3,index-1,index,index+1,animationUnit,img)
        elif(index == 3 and LeftOn == 1):
            AnimationLeftCall.animationleft(index-1,index,index+1,index-3,animationUnit,img)
        else:
            if(RightOn == 1):
                AnimationRightCall.animationright(index-2,index-1,index,index+1,animationUnit,img)
            else:
                AnimationLeftCall.animationleft(index-1,index,index+1,index+2,animationUnit,img)
        if(animationUnit == 9):
            if(index == 0 and RightOn == 1):
                index = 4
                move = 0

            elif(index == 4 and LeftOn == 1):
                index = 0
                move = 0
            else:
                if(RightOn == 1):
                    index = index -1
                    move = 0

                if(LeftOn == 1):
                    index = index +1
                    move = 0
            animationUnit = 0
            move = 0

        timeright = timeright + 1
        timeLeft = timeLeft + 1
        print("leftasdasdsa",LeftOn)
        print("rightasdasdsa",RightOn)
        cv2.imshow('wqzxcq',rightButtonFrame)
        cv2.imshow('funsadasd',leftButtonFrame)
        cv2.imshow('sjdwnmanmd',overlayButtonFrame)
        cv2.imshow('asdasda',img)
        whiteNumRight = 0
        whiteNumLeft = 0
        k = cv2.waitKey(10)
        if k==27:
            break

    cv2.destroyAllWindows()

#SelectClothes()
