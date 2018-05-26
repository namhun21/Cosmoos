import cv2
import sys
import numpy as np
import time
import os
import UI_Sub
import Function
import overlay
import threading
import queue
import Suggest_Color
import Suggest_Pattern


def Third_Menu(cap):
    bottomLeftCornerOfText_Title = (100,200)
    face_pattern = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    clothes = ['hood-t_black_NIKE_M_7000_dot_.png', 'hood-t_black_NIKE_M_7000_printing_.png', 'hood-t_blue_NIKE_M_7000_printing_.png', 'hood-t_gray_NIKE_M_7000_basic_.png', 'hood-t_white_NIKE_M_7000_basic_.png','t-shirt_beige_NIKE_M_7000_basic_.png', 't-shirt_beige_NIKE_M_7000_printing_.png', 't-shirt_beige_NIKE_M_7000_stripe_.png', 't-shirt_black_NIKE_M_7000_stripe_.png', 't-shirt_gray_NIKE_M_7000_dot_.png','t-shirt_gray_NIKE_M_7000_printing_.png','t-shirt_gray_NIKE_M_7000_stripe_.png','t-shirt_white_NIKE_M_7000_printing_.png','y-shirt_beige_NIKE_M_7000_dot_.png', 'y-shirt_black_GUZZI_M_7500_basic_.png', 'y-shirt_blue_NIKE_M_7000_basic_.png', 'y-shirt_blue_NIKE_M_7000_dot_.png', 'y-shirt_blue_NIKE_M_7000_stripe_.png','y-shirt_white_NIKE_M_7000_dot_.png','y-shirt_white_NIKE_M_7000_stripe_.png']
    check = 0
    re = 0
    best_clothes = 'default'
    my_q = queue.Queue()
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceList = face_pattern.detectMultiScale(gray, 1.5)

        if check == 0:
            t = threading.Thread(target = Suggest_Color.Suggest_color, args=(frame, faceList, my_q))
            t.start()   #추천시스템 쓰레드
            check = 1
        img = cv2.flip(frame,1)

        cv2.putText(img,'Loading```````',
                bottomLeftCornerOfText_Title,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255,255,255),
                2)

        cv2.imshow('video', img)
        print('Main')
        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력시 종료
            break
        if check == 1 and t.isAlive() == False:
            t = threading.Thread(target = Suggest_Pattern.Suggest_pattern, args=(frame, faceList, my_q))
            t.start()   #추천시스템 쓰레드
            check = 2
            
            
        if check == 2 and t.isAlive() == False:
            color = my_q.get()
            pattern = my_q.get()
            print(color)   #추천결과
            print(pattern)
            
            for i in range(20) :   #오버레이로 이동
                if(clothes[i].split("_")[1] == color and clothes[i].split("_")[5] == pattern):                          #overlay.Fulloverlay
                    best_clothes = clothes[i]
            print(best_clothes)
            title = best_clothes.split("_")[0]
            print(title)
            overlay.Full_Overlay(cap,best_clothes,title)
    cv2.destroyAllWindows()
    cap.release()
                                 


            
                                 
                                 
    

cap = cv2.VideoCapture(0)
Third_Menu(cap)
