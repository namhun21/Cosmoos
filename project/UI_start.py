import cv2
import sys
import numpy as np
import time
import os
import start2



def draw_Click(frame, position, x1, x2, name):
    font = cv2.FONT_HERSHEY_SIMPLEX
    Position = position
    fontScale = 0.5
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.rectangle(frame, (x1, 50), (x2, 80), (255, 0, 0), 3)
    cv2.putText(frame, name,
                Position,
                font,
                fontScale,
                fontColor,
                lineType)


def make_Roi(gray, x1, y1):
    roi = gray[50:80, x1:y1]
    return roi


def Click_Operation(roi, origraysc, time, count1, count2, count3, num1,num2,num3):
    # num1 = 0
    # num2 = 0
    # num3 = 0

    # time = 0

    # count1 = 0
    # count2 = 0
    # count3 = 0

    for x in range(120):
        for y in range(30):
            oricolor1 = roi[0][y, x]
            roicolor1 = origraysc[0][y, x]
            oricolor2 = roi[1][y, x]
            roicolor2 = origraysc[1][y, x]
            oricolor3 = roi[2][y, x]
            roicolor3 = origraysc[2][y, x]

            if (oricolor1 - roicolor1 < 30):
                roi[0][y, x] = 0
                cv2.imshow
            else:
                roi[0][y, x] = 255
                num1 = num1 + 1
                #print(num1)


            if (oricolor2 - roicolor2 < 30):
                roi[1][y, x] = 0
            else:
                roi[1][y, x] = 255
                num2 = num2 + 1
                #print(num2)

            if (oricolor3 - roicolor3 < 30):
                roi[2][y, x] = 0
            else:
                roi[2][y, x] = 255
                num3 = num3 + 1
            # print(num1,num2,num3)

    if (num1 > 3600 * 0.5 and time > 50):
        count1 = count1 + 1

    num1 = 0

    if (num2 > 3600 * 0.5 and time > 50):
        count2 = count2 + 1

    num2 = 0

    if (num3 > 3600 * 0.5 and time > 50):
        count3 = count3 + 1

    num3 = 0

    return count1, count2, count3,num1,num2,num3,time


def user_Interface():
    cap = cv2.VideoCapture(0)
    # Icon = ['T-Shirt.jpg','Y-Shirt.png','Hood.jpg']
    bottomLeftCornerOfText1 = (460, 70)
    bottomLeftCornerOfText2 = (260, 70)
    bottomLeftCornerOfText3 = (60, 70)


    count1 = 0
    count2 = 0
    count3 = 0

    num1 = 0
    num2 = 0
    num3 = 0

    time = 0
    check = 0
    kernel = np.ones((5, 5), np.uint8)

    while True:
        ret, frame = cap.read()
        frame_copy = frame.copy()

        draw_Click(frame, bottomLeftCornerOfText1, 450, 570, 'T-shirt')
        draw_Click(frame, bottomLeftCornerOfText2, 250, 370, 'Y-shirt')
        draw_Click(frame, bottomLeftCornerOfText3, 50, 170, 'Hood')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        roi1 = make_Roi(gray, 450, 570)
        roi2 = make_Roi(gray, 250, 370)
        roi3 = make_Roi(gray, 50, 170)

        roi = [roi1, roi2, roi3]

        if (check == 0 and time > 100):
            # cap1 = cv2.VideoCapture(0)
            # ret, ori2 = cap1.read()

            # oriroi1 = ori2[50:80,450:570]
            # oriroi2 = ori2[50:80,250:370]
            # oriroi3 = ori2[50:80,50:170]

            origray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            origraysc1 = make_Roi(origray, 450, 570)
            origraysc2 = make_Roi(origray, 250, 370)
            origraysc3 = make_Roi(origray, 50, 170)

            origraysc = [origraysc1, origraysc2, origraysc3]
            cv2.imshow('ori', origraysc3)
            check = 1

        if (check == 1):
            count1, count2, count3, num1,num2,num3, time = Click_Operation(roi, origraysc, time,count1,count2,count3,num1,num2,num3)

        print(count1, count2, count3)

        if (count1 > 20):
            print("success1")
            start2.pou('T-shirt')
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count2 > 20):
            print("success2")
            start2.pou('Y-shirt')
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count3 > 20):
            print("success3")
            start2.pou('Hood-T')
            count1 = 0
            count2 = 0
            count3 = 0

        cv2.imshow('video', frame)
        time = time + 5

        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력시 종료
            break
        elif cv2.waitKey(1) & 0xFF == ord('h'):  # h 입력시 start2에 pou('Hood-T') 실행
            start2.pou('Hood-T')

        elif cv2.waitKey(1) & 0xFF == ord('y'):  # y 입력시 start2에 pou('Y-shirt') 실행
            start2.pou('Y-shirt')

        elif cv2.waitKey(1) & 0xFF == ord('t'):  # t 입력시 start2에 pou('T-shirt') 실행
            start2.pou('T-shirt')

    cv2.destroyAllWindows()
    cap.release()


user_Interface()