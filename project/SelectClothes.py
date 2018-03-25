import cv2
import numpy as np
import AnimationRightCall
import AnimationLeftCall
import Click_Function
import overlay

def SelectClothes(cap):
    TextLocation1=(50, 230)
    TextLocation2=(550, 230)
    TextLocation3=(550, 400)
    #cap = cv2.VideoCapture(0)
    index = 0 #옷의 배열 인덱스
    velocity = 0.5#애니메이션의 속도를 결정함. 0<velocity<2 사이의 값 가능
    overlaycount = 0#손이 올렸을 때 바로 클릭인지되지 않도록 20됐을 때 동작 실행
    LeftOn = 0#애니메이션 왼쪽 오른쪽 구분하기 위하여 선언
    RightOn = 0#애니메이션 왼쪽 오른쪽 구분하기 위하여 선언
    startcompare = 0#영상의 프레임과 이미지 비교 시작
    animationUnit = 0#애니메이션 움직임의 가중치(좌표에 더해지는 값)
    timeright = 0#100번의 루프를 돌고나서 이미지 찍기 위한 변수
    timeLeft = 0#100번의 루프를 돌고나서 이미지 찍기 위한 변수

    move = 0#1일 때 움직임을 허가한다.
    whiteNumLeft = 0#왼쪽 애니메이션  버튼의 흑백 프레임의 흰색 픽셀의 개수
    whiteNumRight = 0#오른쪽 애니메이션  버튼의 흑백 프레임의 흰색 픽셀의 개수
    whiteNumOverlay = 0#가운데 overlay창으로 가기위한 버튼의 흑백 프레임의 흰색 픽셀의 개수

    Clothes_name ='coat_no.png'

    while(cap.isOpened()):
        ret, img = cap.read()
        img1 = cv2.flip(img,1)


        Click_Function.draw_Click(img1,TextLocation1,(10,200),(140,250),"Turn Left")
        Click_Function.draw_Click(img1,TextLocation2,(510,200),(640,250),"Turn Right")
        Click_Function.draw_Click(img1,TextLocation3,(510,380),(640,430),"Overlay")
        #cv2.rectangle(img1,(10,200),(180,250),(255,0,0),3)
        #cv2.rectangle(img1,(200,350),(350,650),(255,0,0),3)
        #cv2.rectangle(img1,(510,250),(640,300),(255,0,0),3)

        imgray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        leftButtonFrame = imgray[200:250,10:140]
        rightButtonFrame = imgray[200:250,510:640]
        overlayButtonFrame = imgray[380:430,510:640]

        if(startcompare == 0 and timeright > 100 and timeLeft > 100):#루프를 100번 돌고나서 비교할 이미지 추출
            picturegray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
            pictureleftButtonFrame = picturegray[200:250,10:140]#왼쪽 애니메이션 버튼 부분
            picturerightButtonFrame = picturegray[200:250,510:640]#오른쪽 애니메이션  버튼 부분
            pictureoverlayButtonFrame = picturegray[380:430,510:640]#가운데 overlay 버튼 부분
            startcompare = 1 #비교 시작

        if(startcompare == 1):#비교하기 위한 이미지 추출
            for x in range(130):
                for y in range(50):
                  picturecolor = rightButtonFrame[y,x]#현재 프레임의 오른쪽 버튼 부분
                  rightButtonFrameColor = picturerightButtonFrame[y,x]#찍어놓은 이미지의 오른쪽 버튼 부분
                  if(picturecolor- rightButtonFrameColor < 30):#비교해서 색의 차가 30 미만일 때
                       rightButtonFrame[y,x] = 0#흑색으로 변환
                  else:
                       rightButtonFrame[y,x] = 255#백색으로 변환
                       whiteNumRight = whiteNumRight+1#오른쪽 부분의 흰색 픽셀 개수 증가

            for x in range(130):
                for y in range(50):
                  picturecolor = leftButtonFrame[y,x]#현재 프레임의 왼쪽 버튼 부분
                  leftButtonFrameColor = pictureleftButtonFrame[y,x]#찍어놓은 이미지의 왼쪽 버튼 부분
                  if(picturecolor - leftButtonFrameColor < 30):#비교해서 색의 차가 30 미만일 때
                       leftButtonFrame[y,x] = 0#흑색으로 변환
                  else:
                       leftButtonFrame[y,x] = 255#백색으로 변환
                       whiteNumLeft = whiteNumLeft+1#왼쪽 부분의 흰색 픽셀 개수 증가


            for x in range(130):
                for y in range(50):
                  picturecolor = overlayButtonFrame[y,x]#현재 프레임의 가운데 버튼 부분
                  overlayButtonColor = pictureoverlayButtonFrame[y,x]#찍어놓은 이미지의 가운데 버튼 부분
                  if(picturecolor- overlayButtonColor < 30):#비교해서 색의 차가 30 미만일 때
                       overlayButtonFrame[y,x] = 0#흑색으로 변환
                  else:
                       overlayButtonFrame[y,x] = 255#백색으로 변환
                       whiteNumOverlay = whiteNumOverlay+1#가운데 부분의 흰색 픽셀 개수 증가


        if(whiteNumRight > 6500 *0.7):
            LeftOn = 0
            RightOn = 1
            move = 1

        if(whiteNumLeft > 6500*0.7):
           LeftOn = 1
           RightOn = 0
           move = 1

        if(whiteNumOverlay > 6500 *0.7):
            overlaycount = overlaycount + 1
        else:
            overlaycount = 0



        if(move == 1):#애니메이션 가동 시작
            animationUnit = animationUnit + velocity#가중치를 증가

        if(index == 0):#가운데 이미지의 배열 인덱스가 0일 시의 예외 처리
            if(RightOn == 1):
                Clothes_name = AnimationRightCall.animationright(index+3,index+4,index,index+1,animationUnit,img1)
            else:
                Clothes_name = AnimationLeftCall.animationleft(index+4,index,index+1,index+2,animationUnit,img1)   #hm

        elif(index == 4):#가운데 이미지의 배열 인덱스가 4일 시의 예외 처리
            if(RightOn == 1):
                Clothes_name = AnimationRightCall.animationright(index-2,index-1,index,index-4,animationUnit,img1)
            else:
                Clothes_name = AnimationLeftCall.animationleft(index-1,index,index-4,index-3,animationUnit,img1)
        elif(index == 1 and RightOn == 1):#가운데 이미지의 배열 인덱스가 1일 시의 예외 처리
            Clothes_name=AnimationRightCall.animationright(index+3,index-1,index,index+1,animationUnit,img1)
        elif(index == 3 and LeftOn == 1):#가운데 이미지의 배열 인덱스가 3일 시의 예외 처리
            Clothes_name=AnimationLeftCall.animationleft(index-1,index,index+1,index-3,animationUnit,img1)
        else:#예외를 제외한 나머지 부분의 애니메이션 함수
            if(RightOn == 1):
                Clothes_name=AnimationRightCall.animationright(index-2,index-1,index,index+1,animationUnit,img1)
            else:
                Clothes_name=AnimationLeftCall.animationleft(index-1,index,index+1,index+2,animationUnit,img1)   #hm
        if(animationUnit >= 9):#애니메이션 완료 시
            if(index == 0 and RightOn == 1):#가운데 이미지 인덱스가 0일 때 오른쪽 애니메이션 가동 중지
                index = 4
                move = 0

            elif(index == 4 and LeftOn == 1):#가운데 이미지 인덱스가 4일 때 왼쪽  애니메이션 가동 중지
                index = 0
                move = 0
            else:#예외를 제외한 애니메이션 가동 중지
                if(RightOn == 1):
                    index = index -1
                    move = 0

                if(LeftOn == 1):
                    index = index +1
                    move = 0
            animationUnit = 0
            move = 0

        timeright = timeright + 1#비교할 프레임을 찍기위한 시간 체크변수 1증가(100때 이미지 비교 시작)
        timeLeft = timeLeft + 1#비교할 프레임을 찍기위한 시간 체크변수 1증가(100때 이미지 비교 시작)
        #print(whiteNumLeft)
        #print(whiteNumRight)
        #print(overlaycount)
        #print('출력: ',Clothes_name)
        if(overlaycount == 20):#오버레이 창으로 전환
            overlaycount = 0
            overlay.Full_Overlay(cap,Clothes_name)
        #cv2.imshow('wqzxcq',rightButtonFrame)
        #cv2.imshow('funsadasd',leftButtonFrame)
        #cv2.imshow('sjdwnmanmd',overlayButtonFrame)
        cv2.imshow('video',img1)
        whiteNumRight = 0#흰색 픽셀의 개수 초기화
        whiteNumLeft = 0#흰색 픽셀의 개수 초기화
        whiteNumOverlay = 0#흰색 픽셀의 개수 초기화
        k = cv2.waitKey(10)
        if k==27:
            break

    cv2.destroyAllWindows()


cap = cv2.VideoCapture(0)
SelectClothes(cap)


