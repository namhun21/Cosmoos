import cv2
import numpy as np
import AnimationRightCall
import AnimationLeftCall
import Function
import overlay
import UI_Start
import os
import Make_Clothes_Image
import time_measurement
import time

def SelectClothes(title, cap):

    frame_number = 1
    index = 0 #옷의 배열 인덱스
    velocity = 1.8#애니메이션의 속도를 결정함. 0<velocity<2 사이의 값 가능
    overlaycount = 0#손이 올렸을 때 바로 클릭인지되지 않도록 20됐을 때 동작 실행
    backcount = 0#손이 올렸을 때 바로 클릭인지되지 않도록 20됐을 때 동작 실행
    LeftOn = 0#애니메이션 왼쪽 오른쪽 구분하기 위하여 선언
    RightOn = 0#애니메이션 왼쪽 오른쪽 구분하기 위하여 선언
    startcompare = 0#영상의 프레임과 이미지 비교 시작
    animationUnit = 0#애니메이션 움직임의 가중치(좌표에 더해지는 값)
    waiting_time = 0#100번의 루프를 돌고나서 이미지 찍기 위한 변수
    
    
    

    move = 0#1일 때 움직임을 허가한다.
    whiteNumLeft = 0#왼쪽 애니메이션  버튼의 흑백 프레임의 흰색 픽셀의 개수
    whiteNumRight = 0#오른쪽 애니메이션  버튼의 흑백 프레임의 흰색 픽셀의 개수
    whiteNumOverlay = 0#가운데 overlay창으로 가기위한 버튼의 흑백 프레임의 흰색픽셀의 개수
    sum_time = 0
    n = 0
    # kinds = title.split("_")[0][0]
    kinds = title[0]
    if(kinds == 'h'):
        clothes = ['hood-t_black_NIKE_M_7000_dot_.png', 'hood-t_black_NIKE_M_7000_printing_.png', 'hood-t_blue_NIKE_M_7000_printing_.png', 'hood-t_gray_NIKE_M_7000_basic_.png', 'hood-t_white_NIKE_M_7000_basic_.png']
    elif(kinds == 't'):
        clothes = ['t-shirt_beige_NIKE_M_7000_basic_.png', 't-shirt_beige_NIKE_M_7000_printing_.png', 't-shirt_beige_NIKE_M_7000_stripe_.png', 't-shirt_black_NIKE_M_7000_stripe_.png', 't-shirt_gray_NIKE_M_7000_dot_.png','t-shirt_gray_NIKE_M_7000_printing_.png','t-shirt_gray_NIKE_M_7000_stripe_.png','t-shirt_white_NIKE_M_7000_printing_.png']
    else:
        clothes = ['y-shirt_beige_NIKE_M_7000_dot_.png', 'y-shirt_black_GUZZI_M_7500_basic_.png', 'y-shirt_blue_NIKE_M_7000_basic_.png', 'y-shirt_blue_NIKE_M_7000_dot_.png', 'y-shirt_blue_NIKE_M_7000_stripe_.png','y-shirt_white_NIKE_M_7000_dot_.png','y-shirt_white_NIKE_M_7000_stripe_.png']


    while(cap.isOpened()):

        ret, img = cap.read()
        img1 = cv2.flip(img,1)
        Make_Clothes_Image.make_Button_Image('left.png', (100, 50), 200, 250, 40, 140, img1)
        Make_Clothes_Image.make_Button_Image('right.png', (100, 50), 200, 250, 510, 610, img1)
        Make_Clothes_Image.make_Button_Image('back(64).png', (50, 50), 380, 430, 60, 110, img1)
        Make_Clothes_Image.make_Clothes_Image('clothes.png', (100, 50), 380, 430, 510, 610, img1)


        imgray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

        if(startcompare == 0 and waiting_time > 300):#루프를 100번 돌고나서 비교할 이미지 추출
            picturegray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
            pictureleftButtonFrame = picturegray[200:250,40:140]#왼쪽 애니메이션 버튼 부분
            picturerightButtonFrame = picturegray[200:250,510:610]#오른쪽 애니메이션  버튼 부분
            pictureoverlayButtonFrame = picturegray[380:430,510:610]#가운데 overlay 버튼 부분
            picturebackButtonFrame = picturegray[380:430,40:140]#뒤로가기 버튼 부분
           # cv2.imshow('sadas',picturerightButtonFrame)
            startcompare = 1 #비교 시작

        if(startcompare == 1 and frame_number == 1):#비교하기 위한 이미지 추출
            rightButtonFrame = imgray[200:250,510:610]
            whiteNumRight = Function.Select_Click_Operation(rightButtonFrame,picturerightButtonFrame,100,50)
            if(whiteNumRight > 5000 *0.4):
                LeftOn = 0
                RightOn = 1
                move = 1
        if(startcompare == 1 and frame_number == 2):
            leftButtonFrame = imgray[200:250,40:140]
            whiteNumLeft = Function.Select_Click_Operation(leftButtonFrame,pictureleftButtonFrame,100,50)
            if(whiteNumLeft > 5000*0.4):
                LeftOn = 1
                RightOn = 0
                move = 1

        if(startcompare == 1 and frame_number == 3):
            overlayButtonFrame = imgray[380:430,510:610]
            whiteNumOverlay = Function.Select_Click_Operation(overlayButtonFrame,pictureoverlayButtonFrame,100,50)
            if(whiteNumOverlay > 5000 *0.5):
                overlaycount = overlaycount + 1

        if (startcompare == 1 and frame_number == 4):
            backButtonFrame = imgray[380:430, 40:140]
            whiteNumBack = Function.Select_Click_Operation(backButtonFrame, picturebackButtonFrame, 100, 50)
            if (whiteNumBack > 5000 * 0.5):
                backcount = backcount + 1

        if(move == 1):#애니메이션 가동 시작
            animationUnit = animationUnit + velocity#가중치를 증가

        if(kinds == 'h'):
            if(index == 0):#가운데 이미지의 배열 인덱스가 0일 시의 예외 처리
                if(RightOn == 1):
                    Clothes_name = AnimationRightCall.animationright(index+3,index+4,index,index+1,animationUnit,img1,title)
                else:
                    Clothes_name = AnimationLeftCall.animationleft(index+4,index,index+1,index+2,animationUnit,img1,title)   #hm

            elif(index == 4):#가운데 이미지의 배열 인덱스가 4일 시의 예외 처리
                if(RightOn == 1):
                    Clothes_name = AnimationRightCall.animationright(index-2,index-1,index,index-4,animationUnit,img1,title)
                else:
                    Clothes_name = AnimationLeftCall.animationleft(index-1,index,index-4,index-3,animationUnit,img1,title)
            elif(index == 1 and RightOn == 1):#가운데 이미지의 배열 인덱스가 1일 시의 예외 처리
                Clothes_name=AnimationRightCall.animationright(index+3,index-1,index,index+1,animationUnit,img1,title)
            elif(index == 3 and LeftOn == 1):#가운데 이미지의 배열 인덱스가 3일 시의 예외 처리
                Clothes_name=AnimationLeftCall.animationleft(index-1,index,index+1,index-3,animationUnit,img1,title)
            else:#예외를 제외한 나머지 부분의 애니메이션 함수
                if(RightOn == 1):
                    Clothes_name=AnimationRightCall.animationright(index-2,index-1,index,index+1,animationUnit,img1,title)
                else:
                    Clothes_name=AnimationLeftCall.animationleft(index-1,index,index+1,index+2,animationUnit,img1,title)   #hm
            if(abs(animationUnit - 9) <= 1):#애니메이션 완료 시
                if(index == 0 and RightOn == 1):#가운데 이미지 인덱스가 0일 때 오른쪽 애니메이션 가동 중지
                    index = 4


                elif(index == 4 and LeftOn == 1):#가운데 이미지 인덱스가 4일 때 왼쪽  애니메이션 가동 중지
                    index = 0

                else:#예외를 제외한 애니메이션 가동 중지
                    if(RightOn == 1):
                        index = index -1


                    if(LeftOn == 1):
                        index = index +1

                animationUnit = 0
                move = 0
        else:
            if (index == 0):  # 가운데 이미지의 배열 인덱스가 0일 시의 예외 처리
                if (RightOn == 1):
                    Clothes_name = AnimationRightCall.animationright(index + 5, index + 6, index, index + 1,
                                                                     animationUnit, img1, title)
                else:
                    Clothes_name = AnimationLeftCall.animationleft(index + 6, index, index + 1, index + 2,
                                                                   animationUnit, img1, title)  # hm

            elif (index == 6):  # 가운데 이미지의 배열 인덱스가 4일 시의 예외 처리
                if (RightOn == 1):
                    Clothes_name = AnimationRightCall.animationright(index - 2, index - 1, index, index - 6,
                                                                     animationUnit, img1, title)
                else:
                    Clothes_name = AnimationLeftCall.animationleft(index - 1, index, index - 6, index - 5,
                                                                   animationUnit, img1, title)
            elif (index == 1 and RightOn == 1):  # 가운데 이미지의 배열 인덱스가 1일 시의 예외 처리
                Clothes_name = AnimationRightCall.animationright(index + 5, index - 1, index, index + 1, animationUnit,
                                                                 img1, title)
            elif (index == 5 and LeftOn == 1):  # 가운데 이미지의 배열 인덱스가 3일 시의 예외 처리
                Clothes_name = AnimationLeftCall.animationleft(index - 1, index, index + 1, index - 5, animationUnit,
                                                               img1, title)
            else:  # 예외를 제외한 나머지 부분의 애니메이션 함수
                if (RightOn == 1):
                    Clothes_name = AnimationRightCall.animationright(index - 2, index - 1, index, index + 1,
                                                                     animationUnit, img1, title)
                else:
                    Clothes_name = AnimationLeftCall.animationleft(index - 1, index, index + 1, index + 2,
                                                                   animationUnit, img1, title)  # hm
            if (abs(animationUnit - 9) <= 1):  # 애니메이션 완료 시
                if (index == 0 and RightOn == 1):  # 가운데 이미지 인덱스가 0일 때 오른쪽 애니메이션 가동 중지
                    index = 6


                elif (index == 6 and LeftOn == 1):  # 가운데 이미지 인덱스가 4일 때 왼쪽  애니메이션 가동 중지
                    index = 0

                else:  # 예외를 제외한 애니메이션 가동 중지
                    if (RightOn == 1):
                        index = index - 1

                    if (LeftOn == 1):
                        index = index + 1

                animationUnit = 0
                move = 0

        waiting_time = waiting_time + 3#비교할 프레임을 찍기위한 시간 체크변수 5증가(100때 이미지 비교 시작)

        if(overlaycount == 20):#오버레이 창으로 전환
            overlaycount = 0
            overlay.Full_Overlay(cap,clothes[Clothes_name],title)
            break
        if(backcount == 20):
            backcount = 0
            UI_Start.First_Menu(cap)

        cv2.imshow('video',img1)

        whiteNumRight = 0#흰색 픽셀의 개수 초기화
        whiteNumLeft = 0#흰색 픽셀의 개수 초기화
        whiteNumOverlay = 0#흰색 픽셀의 개수 초기화
        if(frame_number <4):
            frame_number = frame_number + 1
        else:
            frame_number = 1
        k = cv2.waitKey(10)
        if k==27:
            break

        #Select_endTime = int(round(time.time() * 1000))
        #sum_time,n = time_measurement.measure(Select_startTime, Select_endTime, sum_time, n)


    cv2.destroyAllWindows()

# cap = cv2.VideoCapture(0)
# SelectClothes('t-shirt', cap)




