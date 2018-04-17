import cv2
import sys
import numpy as np
import time
import os
import Function
import time_measurement

prev_x = 0
prev_y = 0
prev_w = 0
prev_h = 0

def masked_Operation(x,y,w,h,img,body_mask,Clothes_name,img_size,store): # 상체 ROI의 범위를 정하고 이미지를 해당 영역에 덮어씌운다

    if x>20:
        x = x-10
    y_offset = 130    # 이미지 사이즈 조정


    frame_roi = img[y+y_offset:y+y_offset+img_size, x:x+img_size]
    if(store == 0):
        cv2.imshow('video2',frame_roi)

    body_mask_small = cv2.resize(body_mask,(img_size,img_size),interpolation = cv2.INTER_CUBIC) # 옷이미지 키우기
    gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)# 키운 이미지의 gray처리 (BGR->Gray)

    color = Clothes_name.split("_")[1]
    if((color == "black") or (color == "blue") or (color == "red")):
        ret, mask = cv2.threshold(gray_mask, 200,255, cv2.THRESH_BINARY_INV)
    else:
        ret, mask = cv2.threshold(gray_mask, 1,255, cv2.THRESH_BINARY)

    mask_inv = cv2.bitwise_not(mask)

    try:        # bitwise_and부분에서 error가 발생하는 경우가 있기때문에 그경우에는 Error를 출력하게 하고 그외에는 그대로 실행시킨다.
        masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask) # 오버레이되는 부분만 남게된다.
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv) #배경만 남게된다
        img[y+y_offset:y+y_offset+img_size, x:x+img_size] = cv2.add(masked_body, masked_frame) # 화면에 이미지 오버레이
        if(store ==1):
            if(color == "black"):
                cv2.imwrite('overlay_black.png', img)
            elif(color == "blue"):
                cv2.imwrite('overlay_blue.png', img)
            elif(color == "red"):
                cv2.imwrite('overlay_red.png', img)
            elif(color == "white"):
                cv2.imwrite('overlay_white.png', img)
            else :
                cv2.imwrite('overlay_yellow.png', img)
            
    except:
        print('Error')
        

def Range_Operation(body,img,body_mask,Clothes_name,img_size):    # 특정조건에서만 실행되도록 조건을 부여하였다
    count = 0
    global prev_x
    global prev_y
    global prev_w
    global prev_h

    for (x, y, w, h) in body:

        #print('x = ',x,'y = ',y,'w = ',w,'h = ',h)

        if (abs(prev_x-x) < 10) and (abs(prev_y-y) < 10): #이전 x,y 와 현재 x,y의 차이가 별로 나지 않으면 이전 위치의 이미지 출력
            #print('prev_x =', prev_x, 'x = ', x, 'prev_y = ',prev_y, 'y = ', y, 'w= ',prev_w, 'h = ',prev_h)
            continue

        if (prev_w != 0):
            if (abs(prev_w-w) > 20) and (abs(prev_h-h) > 20):
                #print('prev_w = ',prev_w,'w = ',w,'prev_h = ',prev_h,'h = ',h)
                continue

        count = count + 1
        if(count >= 2):
            break
        #print('x= ',x,'y= ',y,'w= ',w,'h= ',h)

        prev_x = x
        prev_y = y
        prev_w = w
        prev_h = h

        if  (x>20 and x<520):     # 특정 영역을 벗어나지 않으면 오버레이
            masked_Operation(x,y,w,h,img,body_mask,Clothes_name,img_size,0)

        else:
            continue


    if (count == 0):   # 이동 전, 후 차이가 적으면 이전 오버레이위치 출력
        if (prev_x !=0 and prev_y !=0 and prev_w != 0 and prev_h !=0):
            masked_Operation(prev_x,prev_y,prev_w,prev_h,img,body_mask,Clothes_name,img_size, 0)

        #cv2.rectangle(frame,(prev_x,prev_y),(prev_x+prev_w,prev_y+prev_h),(0,255,255),2)
        #draw_shirt(x,y,w,h)

def Full_Overlay(cap,Clothes_name):       #이전에 정의했던 함수들을 모아서 처리

    Clothes_name = Clothes_name
    bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')    #학습데이터 읽어오기

    TextPosition = ((540,130),(540,270),(540,390)) # 글씨가 적혀질 위치
    TextPosition1 = ((50,250),(50,370)) # Up, Down 글씨가 적힐 위치
    InfoPosition = ((20, 80),(20, 120),(20, 160)) #옷 브랜드, 사이즈, 가격 순서


    backButtonCount = 0  #손이 올렸을 때 바로 클릭인지되지 않도록 20됐을 때 동작 실행하도록하는 변수
    startcompare = 0   #영상의 프레임과 이미지 비교 시작
    timeright = 0#100번의 루프를 돌고나서 이미지 찍기 위한 변수
    timeLeft = 0#100번의 루프를 돌고나서 이미지 찍기 위한 변수

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0

    frame_number = 1

    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0

    waiting_time = 0
    check = 0
    sum_time = 0
    n = 0
    img_size = 260
    body_mask = cv2.imread(Clothes_name)  #애니메이션함수로 부터 이미지의 이름을 받아 이미지 읽어오기

    # h_mask, w_mask = body_mask.shape[:2] #이미지 영역

    if bodyCascade.empty(): #학습데이터 없을시 에러메세지
        raise IOError('Unable to load the mouth cascade classifier xml files')

    while True:
        Overlay_startTime = int(round(time.time() * 1000))
        # Capture frame-by-frame
        ret, frame = cap.read()
        #frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_CUBIC)
        img = cv2.flip(frame,1)  #카메라 반전

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # BGR-> Gray

        body = bodyCascade.detectMultiScale(
            gray,
            minSize=(100,200),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        Function.draw_Click(img,TextPosition[0],(500,100),(620,150),'Reco')
        Function.draw_Click(img,TextPosition[1],(500,250),(620,300),'List')
        #Function.draw_Click(img,TextPosition[2],(500,350),(620,420),'Back')

        Function.draw_Click(img,TextPosition1[0],(20,230),(120,280),'Up')
        Function.draw_Click(img,TextPosition1[1],(20,350),(120,400),'Down')

        ClothesBrand = 'Brand: ' + Clothes_name.split("_")[2]
        ClothesSize = 'Size: ' + Clothes_name.split("_")[3]
        ClothesPrice = 'Price: ' + Clothes_name.split("_")[4]


        Function.draw_Click(img,InfoPosition[0], (0,0), (0,0), ClothesBrand)
        Function.draw_Click(img,InfoPosition[1], (0,0), (0,0), ClothesSize)
        Function.draw_Click(img,InfoPosition[2], (0,0), (0,0), ClothesPrice)



        Range_Operation(body,img,body_mask,Clothes_name,img_size)

        roi1 = Function.make_Roi(gray, 230, 280, 20, 120)
        roi2 = Function.make_Roi(gray, 350, 400, 20, 120)
        roi3 = Function.make_Roi(gray, 100, 150, 500, 600)
        roi4 = Function.make_Roi(gray, 250, 300, 500, 600)
        roi = [roi1, roi2, roi3, roi4]

        if (check == 0 and waiting_time > 100):  # waiting_time이 100이상이되면 버튼 클릭 인식을 시작한다.
            # 사진을 찍어서 지금 화면과 달라지는 영역을 인식한다.

            origray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            origraysc1 = Function.make_Roi(origray, 230, 280, 20, 120)
            origraysc2 = Function.make_Roi(origray, 350, 400, 20, 120)
            origraysc3 = Function.make_Roi(origray, 100, 150, 500,600)
            origraysc4 = Function.make_Roi(origray, 250, 300, 500,600)

            origraysc = [origraysc1, origraysc2,origraysc3,origraysc4]

            check = 1

        if (check == 1):  # 클릭 함수를 실행시킨다

            if(frame_number == 1):
                count1, num1, waiting_time = Function.overlay_Click_Operation(roi, origraysc, waiting_time, count1, num1, 0)
            if(frame_number==2):
                count2, num2, waiting_time = Function.overlay_Click_Operation(roi, origraysc, waiting_time, count2, num2, 1)
            if(frame_number==3):
                count3, num3, waiting_time = Function.overlay_Click_Operation(roi, origraysc, waiting_time, count3, num3, 2)
            if(frame_number==4):
                count4, num4, waiting_time = Function.overlay_Click_Operation(roi, origraysc, waiting_time, count4, num4, 3)

        cv2.imshow('video', img)

        if (count1 > 20):  # count1이 20이 넘으면 UI_Sub에 있는 Second_Menu를 실행시킨다.
            print("success1")
            Clothes_name, img_size = Function.sizeUp(Clothes_name,img_size)
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
        elif (count2 > 20):
            print("success2")
            Clothes_name, img_size = Function.sizeDown(Clothes_name,img_size)
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
        elif (count3 > 20):
            print("success3")
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
        elif (count4 > 20):
            print("success4")
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0

        if(frame_number <4):
            frame_number = frame_number + 1
        else:
            frame_number = 1
        print(Clothes_name,img_size)


        waiting_time = waiting_time + 5

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #Overlay_endTime = int(round(time.time() * 1000))
        #sum_time,n = time_measurement.measure(Overlay_startTime, Overlay_endTime, sum_time, n)


    cv2.destroyAllWindows()
    cap.release()


#cap = cv2.VideoCapture(0)
#Clothes_name= "hood-t_white_NIKE_M_7000_.png"
#Full_Overlay(cap,Clothes_name)
