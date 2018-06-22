import cv2
import sys
import numpy as np
import time
import os
import Function
import SelectClothes
import Make_Clothes_Image
import time_measurement
import UI_Recommend

#overlay에 관한 기초적인 코드는 다 같이 작성하였고 그 외 masked_operation과
#range_operation은 김남훈 학생이 작성하였습니다. 코드의 구조화 역시 김남훈
#학생이 진행하였습니다.


prev_x = 0
prev_y = 0
prev_w = 0
prev_h = 0

def masked_Operation(x,y,w,h,img,body_mask,Clothes_name,img_size,Flag): # 상체 ROI의 범위를 정하고 이미지를 해당 영역에 덮어씌운다

    if x>20:
        x = x-10

    if Flag == 1:
        x = x-10
    elif Flag == 2:
        x = x+10
        
    y_offset = 100    # 이미지 사이즈 조정
    
    x, col, y_offset, img_size = Function.Decision_sizeOffset(Clothes_name, x, y_offset, img_size)
    
    frame_roi = img[y+y_offset:y+y_offset+col, x:x+img_size]
    
    #cv2.imshow('video2',frame_roi)

    body_mask_small = cv2.resize(body_mask,(img_size,col),interpolation = cv2.INTER_CUBIC) # 옷이미지 키우기
    gray_mask = cv2.cvtColor(body_mask_small, cv2.COLOR_BGR2GRAY)# 키운 이미지의 gray처리 (BGR->Gray)

    Clothes_pattern = Clothes_name.split("_")[5]

    mask = Function.Decision_mask(Clothes_name, gray_mask)
        
    mask_inv = cv2.bitwise_not(mask)

    try:        # bitwise_and부분에서 error가 발생하는 경우가 있기때문에 그경우에는 Error를 출력하게 하고 그외에는 그대로 실행시킨다.
        masked_body = cv2.bitwise_and(body_mask_small,body_mask_small, mask = mask) # 오버레이되는 부분만 남게된다.
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask = mask_inv) #배경만 남게된다
        img[y+y_offset:y+y_offset+col, x:x+img_size] = cv2.add(masked_body, masked_frame) # 화면에 이미지 오버레이
        
            
    except:
        print('Error')


def Range_Operation(body,img,body_mask,Clothes_name,img_size,Flag):    # 특정조건에서만 실행되도록 조건을 부여하였다
    count = 0
    global prev_x
    global prev_y
    global prev_w
    global prev_h

    for (x, y, w, h) in body:

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
            masked_Operation(x,y,w,h,img,body_mask,Clothes_name,img_size,Flag)

        else:
            continue


    if (count == 0):   # 이동 전, 후 차이가 적으면 이전 오버레이위치 출력
        if (prev_x !=0 and prev_y !=0 and prev_w != 0 and prev_h !=0):
            masked_Operation(prev_x,prev_y,prev_w,prev_h,img,body_mask,Clothes_name,img_size,Flag)


def Full_Overlay(cap,Clothes_name,title):       #이전에 정의했던 함수들을 모아서 처리

    Clothes_name = Clothes_name
    bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')    #학습데이터 읽어오기

    #path = os.path.abspath(".\\img")
    #os.chdir(path)
    
    InfoPosition = ((20, 400),(20, 430),(20, 460)) #옷 브랜드, 사이즈, 가격 순서
    #TextPosition = ((510,130),(515,280),(520,390)) # 글씨가 적혀질 위치
    
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0

    Flag = 0
    frame_number = 1

    waiting_time = 0
    check = 0
    sum_time = 0
    n = 0
    img_size = 260
    col = img_size
    body_mask = cv2.imread('./image/'+ Clothes_name)  #애니메이션함수로 부터 이미지의 이름을 받아 이미지 읽어오기
    
    # h_mask, w_mask = body_mask.shape[:2] #이미지 영역

    if bodyCascade.empty(): #학습데이터 없을시 에러메세지
        raise IOError('Unable to load the mouth cascade classifier xml files')

    while True:
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        #frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation = cv2.INTER_CUBIC)
        img = cv2.flip(frame,1)  #카메라 반전


        
        Make_Clothes_Image.make_Button_Image_Black('SizeUp.png', (60, 50), 100, 150, 60, 120, img)
        Make_Clothes_Image.make_Button_Image_Black('SizeDown.png', (60, 50), 250, 300, 60, 120, img)
        Make_Clothes_Image.make_Clothes_Image('List.png', (60, 50), 250, 300, 500, 560, img)
        Make_Clothes_Image.make_Clothes_Image('Recommend.png',(60,50), 100, 150, 500, 560, img)
        

        #Function.draw_Click(img,TextPosition[0],(500,100),(560,150),'Reco')
        #Function.draw_Click(img,TextPosition[1],(500,250),(560,300),'List')

        #Function.draw_Click(img,TextPosition1[0],(60,100),(120,150),'Up')
        #Function.draw_Click(img,TextPosition1[1],(60,250),(120,300),'Down')

        ClothesBrand = 'Brand: ' + Clothes_name.split("_")[2]
        ClothesSize = 'Size: ' + Clothes_name.split("_")[3]
        ClothesPrice = 'Price: ' + Clothes_name.split("_")[4]


        Function.draw_Click(img,InfoPosition[0], (0,0), (0,0), ClothesBrand)
        Function.draw_Click(img,InfoPosition[1], (0,0), (0,0), ClothesSize)
        Function.draw_Click(img,InfoPosition[2], (0,0), (0,0), ClothesPrice)




        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        body = bodyCascade.detectMultiScale(
            gray,
            minSize=(100,200),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        Range_Operation(body,img,body_mask,Clothes_name,img_size,Flag)


        roi1 = Function.make_Roi(gray, 100, 150, 60, 120)   #Up
        roi2 = Function.make_Roi(gray, 250, 300, 60, 120)   #Down
        roi3 = Function.make_Roi(gray, 100, 150, 500, 560) # Reco
        roi4 = Function.make_Roi(gray, 250, 300, 500, 560)  #List
        roi = [roi1, roi2, roi3, roi4]
        

        if (check == 0 and waiting_time > 100):  # waiting_time이 100이상이되면 버튼 클릭 인식을 시작한다.
            # 사진을 찍어서 지금 화면과 달라지는 영역을 인식한다.

            origray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            origraysc1 = Function.make_Roi(origray, 100, 150, 60, 120)
            origraysc2 = Function.make_Roi(origray, 250, 300, 60, 120)
            origraysc3 = Function.make_Roi(origray, 100, 150, 500,560)
            origraysc4 = Function.make_Roi(origray, 250, 300, 500,560)

            origraysc = [origraysc1, origraysc2,origraysc3,origraysc4]
            

            check = 1

        if (check == 1):  # 클릭 함수를 실행시킨다
            #cv2.imshow('ori1', origraysc1)
            #cv2.imshow('ori2', origraysc2)
            if(frame_number==1):
                count1 = Function.overlay_Click_Operation("sizeup",roi, origraysc, count1, 0)
            if(frame_number==2):
                count2 = Function.overlay_Click_Operation("sizedown",roi, origraysc, count2, 1)
            if(frame_number==3):
                count3 = Function.overlay_Click_Operation("recommend",roi, origraysc, count3, 2)
            if(frame_number==4):
                count4 = Function.overlay_Click_Operation("gotoselect",roi, origraysc, count4, 3)


        # cv2.imshow('1',roi[0])
        # cv2.imshow('2', roi[1])
        
        # cv2.imshow('3', roi[2])
        # cv2.imshow('4', roi[3])
        # print(count1,count2)
        #print(count1,count2,count3,count4)
        cv2.imshow('video', img)

        if (count1 > 10):  
            print("success1")
            cv2.destroyWindow("sizeup")
            cv2.destroyWindow("sizedown")
            cv2.destroyWindow("recommend")
            cv2.destroyWindow("gotoselect")
            Clothes_name, img_size, Flag= Function.sizeUp(Clothes_name,img_size, Flag)
            count1, count2, count3, count4 = Function.resetCount(count1,count2, count3, count4)
        elif (count2 > 10):
            print("success2")
            cv2.destroyWindow("sizeup")
            cv2.destroyWindow("sizedown")
            cv2.destroyWindow("recommend")
            cv2.destroyWindow("gotoselect")
            Clothes_name, img_size, Flag = Function.sizeDown(Clothes_name,img_size, Flag)
            count1, count2, count3, count4 = Function.resetCount(count1,count2, count3, count4)
        elif (count3 > 10):
            print("success3")
            cv2.destroyWindow("sizeup")
            cv2.destroyWindow("sizedown")
            cv2.destroyWindow("recommend")
            cv2.destroyWindow("gotoselect")
            UI_Recommend.Third_Menu(cap)
        elif (count4 > 10):
            print("success4")
            cv2.destroyWindow("sizeup")
            cv2.destroyWindow("sizedown")
            cv2.destroyWindow("recommend")
            cv2.destroyWindow("gotoselect")
            SelectClothes.SelectClothes(title,cap)

        if(frame_number <4):
            frame_number = frame_number + 1
        else:
            frame_number = 1
            
        #print(Clothes_name,img_size)

        waiting_time = waiting_time + 5

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()


os.system("sudo modprobe bcm2835-v4l2")

cap = cv2.VideoCapture(0)
print('width:{0},height:{1}'.format(cap.get(3),cap.get(4)))
cap.set(3,640)
cap.set(4,480)
Clothes_name= "y-shirt_white_NIKE_M_7000_stripe_.png"
Full_Overlay(cap,Clothes_name,"y-shirt")
