import cv2
import sys
import numpy as np
import time
import os
import UI_Sub
import Function


def First_Menu(cap):
    
    bottomLeftCornerOfText1 = (460, 70)
    bottomLeftCornerOfText2 = (260, 70)
    bottomLeftCornerOfText3 = (60, 70)

    count1 = 0
    count2 = 0
    count3 = 0
    
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
        Function.draw_Click(img, bottomLeftCornerOfText1, (450, 50), (570, 80), 'T-shirt')
        Function.draw_Click(img, bottomLeftCornerOfText2, (250, 50), (370, 80), 'Y-shirt')
        Function.draw_Click(img, bottomLeftCornerOfText3, (50, 50), (170, 80), 'Hood')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        roi1 = Function.make_Roi(gray, 50, 80, 450, 570)
        roi2 = Function.make_Roi(gray, 50, 80, 250, 370)
        roi3 = Function.make_Roi(gray, 50, 80, 50, 170)
        roi = [roi1, roi2, roi3]

        if (check == 0 and waiting_time > 100):  # waiting_time이 100이상이되면 버튼 클릭 인식을 시작한다.
            # 사진을 찍어서 지금 화면과 달라지는 영역을 인식한다.
            
            origray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            origraysc1 = Function.make_Roi(origray, 50, 80, 450, 570)
            origraysc2 = Function.make_Roi(origray, 50, 80, 250, 370)
            origraysc3 = Function.make_Roi(origray, 50, 80, 50, 170)

            origraysc = [origraysc1, origraysc2, origraysc3]

            check = 1

        if (check == 1):  # 클릭 함수를 실행시킨다

            if(frame_number == 1):
                count1 = Function.Menu_Click_Operation(roi, origraysc, count1, 0)
            if(frame_number==2):
                count2 = Function.Menu_Click_Operation(roi, origraysc, count2, 1)
            if(frame_number == 3):
                count3 = Function.Menu_Click_Operation(roi, origraysc, count3, 2)


        if (count1 > 20):  # count1이 20이 넘으면 UI_Sub에 있는 Second_Menu를 실행시킨다.
            print("success1")
            UI_Sub.Second_Menu('t-shirt', cap)
        elif (count2 > 20):
            print("success2")
            UI_Sub.Second_Menu('y-shirt', cap)
        elif (count3 > 20):
            print("success3")
            UI_Sub.Second_Menu('hood-t', cap)

        if(frame_number <3):
            frame_number = frame_number + 1
        else:
            frame_number = 1
            
        cv2.imshow('video', img)

        waiting_time = waiting_time + 5
        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력시 종료
            break

    cv2.destroyAllWindows()
    cap.release()




