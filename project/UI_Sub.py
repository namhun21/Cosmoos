import cv2
import sys
import numpy as np
import time
import os
import UI_start
import UI_Recommand



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


def Click_Operation(roi, origraysc, time):
    num1 = 0
    num2 = 0
    num3 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    time = 0
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
            else:
                roi[0][y, x] = 255
                num1 = num1 + 1
            if (oricolor2 - roicolor2 < 30):
                roi[1][y, x] = 0
            else:
                roi[1][y, x] = 255
                num2 = num2 + 1
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

    return count1, count2, count3


def user_Interface(title):
    cap = cv2.VideoCapture(0)
    # Icon = ['T-Shirt.jpg','Y-Shirt.png','Hood.jpg']

    bottomLeftCornerOfText1 = (460, 70)
    bottomLeftCornerOfText2 = (260, 70)
    bottomLeftCornerOfText3 = (60, 70)
    # num1 = 0
    # num2 = 0
    # num3 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    time = 0
    check = 0
    kernel = np.ones((5, 5), np.uint8)

    while True:
        ret, frame = cap.read()

        cv2.putText(frame,title,
                    (0,20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5
                    (255,255,255),
                    2)

        draw_Click(frame, bottomLeftCornerOfText1, 450, 570, 'Recommand')
        draw_Click(frame, bottomLeftCornerOfText2, 250, 370, 'List')
        draw_Click(frame, bottomLeftCornerOfText3, 50, 170, 'Back')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        roi1 = make_Roi(gray, 450, 570)
        roi2 = make_Roi(gray, 250, 370)
        roi3 = make_Roi(gray, 50, 170)

        roi = [roi1, roi2, roi3]

        if (check == 0 and time > 100):
            cap1 = cv2.VideoCapture(0)
            ret, ori2 = cap1.read()

            # oriroi1 = ori2[50:80,450:570]
            # oriroi2 = ori2[50:80,250:370]
            # oriroi3 = ori2[50:80,50:170]

            origray = cv2.cvtColor(ori2, cv2.COLOR_BGR2GRAY)

            origraysc1 = make_Roi(origray, 450, 570)
            origraysc2 = make_Roi(origray, 250, 370)
            origraysc3 = make_Roi(origray, 50, 170)

            origraysc = [origraysc1, origraysc2, origraysc3]

            check = 1

        if (check == 1):
            count1, count2, count3 = Click_Operation(roi, origraysc, time)

        print(count1, count2, count3)

        if (count1 > 20):
            print("success1")
            UI_Recommand.user_Interface('Recommand')
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count2 > 20):
            print("success2")
            UI_Recommand.user_Interface('List')
            count1 = 0
            count2 = 0
            count3 = 0
        elif (count3 > 20):
            print("success3")
            UI_start.user_Interface()
            count1 = 0
            count2 = 0
            count3 = 0

        cv2.imshow('video', frame)
        time = time + 1

        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력 시 종료
            break
        elif cv2.waitKey(1) & 0xFF == ord('b'):  # b 입력 시 이전 페이지로 이동
            start2.pou('Hood-T')

        elif cv2.waitKey(1) & 0xFF == ord('r'):  # r 입력 시 추천 페이지로 이동
            start2.pou('Y-shirt')

        elif cv2.waitKey(1) & 0xFF == ord('l'):  # l 입력 시 목록화면 페이지로 이동
            start2.pou('T-shirt')

    cv2.destroyAllWindows()
    cap.release()
