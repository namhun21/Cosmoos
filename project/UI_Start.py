import cv2
import sys
import numpy as np
import time
import os
import Function
import SelectClothes
import Make_Clothes_Image
import UI_Recommend

#이부분 코딩은 다 같이 함께 했습니다. 기본적 구조를 김동균 학생이 설계하였고 김남훈 학생이 코드의 구조화를 진행하였고
#정재진 학생과 김남훈 학생이 코드를 좀 더 효율적으로 돌아가게 발전 시켰습니다. 차재성 학생은 코드를 세밀하게 만들었습니다.

def First_Menu(cap):

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    
    frame_number = 1
    
    sum_time = 0
    n = 0

    waiting_time = 0
    check = 0
    kernel = np.ones((5, 5), np.uint8)

    while True:

        ret, frame = cap.read()
        img = cv2.flip(frame, 1)


        # 클릭 버튼 만들기
        Make_Clothes_Image.make_Clothes_Image('hood.png', (70, 70), 30, 100, 30, 100, img)
        Make_Clothes_Image.make_Clothes_Image('yshirt.png', (70, 70), 30, 100, 190, 260, img)
        Make_Clothes_Image.make_Clothes_Image('tshirt.png', (70, 70), 30, 100, 350, 420, img)
        Make_Clothes_Image.make_Clothes_Image('Recommend.png', (70, 70), 30, 100, 510, 580, img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        roi1 = Function.make_Roi(gray, 30, 100, 30, 100)
        roi2 = Function.make_Roi(gray, 30, 100, 190, 260)
        roi3 = Function.make_Roi(gray, 30, 100, 350, 420)
        roi4 = Function.make_Roi(gray, 30, 100, 510, 580)
        roi = [roi1, roi2, roi3, roi4]

        if (check == 0 and waiting_time > 100):  # waiting_time이 100이상이되면 버튼 클릭 인식을 시작한다.
            # 사진을 찍어서 지금 화면과 달라지는 영역을 인식한다.
            
            origray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            origraysc1 = Function.make_Roi(origray, 30, 100, 30,100)
            origraysc2 = Function.make_Roi(origray, 30, 100, 190,260)
            origraysc3 = Function.make_Roi(origray, 30, 100, 350, 420)
            origraysc4 = Function.make_Roi(origray, 30,100,510,580)

            origraysc = [origraysc1, origraysc2, origraysc3, origraysc4]

            check = 1

        if (check == 1):  # 클릭 함수를 실행시킨다

            if(frame_number == 1):
                count1 = Function.Menu_Click_Operation("hood-t", roi, origraysc, count1, 0)
            if(frame_number==2):
                count2 = Function.Menu_Click_Operation("y-shirt",roi, origraysc, count2, 1)
            if(frame_number == 3):
                count3 = Function.Menu_Click_Operation("t-shirt",roi, origraysc, count3, 2)
            if(frame_number == 4):
                count4 = Function.Menu_Click_Operation("recommend",roi, origraysc, count4, 3)

        if (count1 > 20):  # count1이 20이 넘으면 UI_Sub에 있는 Second_Menu를 실행시킨다.
            print("success1")
            cv2.destroyWindow("hood-t")
            cv2.destroyWindow("y-shirt")
            cv2.destroyWindow("t-shirt")
            cv2.destroyWindow("recommend")
            SelectClothes.SelectClothes('hood-t', cap)
            break
        elif (count2 > 20):
            print("success2")
            cv2.destroyWindow("hood-t")
            cv2.destroyWindow("y-shirt")
            cv2.destroyWindow("t-shirt")
            cv2.destroyWindow("recommend")
            SelectClothes.SelectClothes('y-shirt', cap)
            break
        elif (count3 > 20):
            print("success3")
            cv2.destroyWindow("hood-t")
            cv2.destroyWindow("y-shirt")
            cv2.destroyWindow("t-shirt")
            cv2.destroyWindow("recommend")
            SelectClothes.SelectClothes('t-shirt', cap)
            break
        elif (count4 > 20):
            print("success4")
            cv2.destroyWindow("hood-t")
            cv2.destroyWindow("y-shirt")
            cv2.destroyWindow("t-shirt")
            cv2.destroyWindow("recommend")
            UI_Recommend.Third_Menu(cap)
            break

        if(frame_number < 4):
            frame_number = frame_number + 1
        else:
            frame_number = 1

        # cv2.namedWindow('video', cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
        cv2.imshow('video', img)

        waiting_time = waiting_time + 5
        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력시 종료
            break

    cv2.destroyAllWindows()
    cap.release()




