import cv2
import sys
import numpy as np
import time
import os
import Function
import overlay
import threading
import queue
import Suggest_Color
import Suggest_Pattern


#김동균 학생이 코드를 작성하였습니다.
def Third_Menu(cap):
    bottomLeftCornerOfText_Title = (0,100)
    face_pattern = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')
    clothes = ['hood-t_black_NIKE_M_7000_dot_.png', 'hood-t_black_NIKE_M_7000_printing_.png', 'hood-t_blue_NIKE_M_7000_printing_.png', 'hood-t_gray_NIKE_M_7000_basic_.png', 'hood-t_white_NIKE_M_7000_basic_.png','t-shirt_beige_NIKE_M_7000_basic_.png', 't-shirt_beige_NIKE_M_7000_printing_.png', 't-shirt_beige_NIKE_M_7000_stripe_.png', 't-shirt_black_NIKE_M_7000_stripe_.png', 't-shirt_gray_NIKE_M_7000_dot_.png','t-shirt_gray_NIKE_M_7000_printing_.png','t-shirt_gray_NIKE_M_7000_stripe_.png','t-shirt_white_NIKE_M_7000_printing_.png','y-shirt_beige_NIKE_M_7000_dot_.png', 'y-shirt_black_GUZZI_M_7500_basic_.png', 'y-shirt_blue_NIKE_M_7000_basic_.png', 'y-shirt_blue_NIKE_M_7000_dot_.png', 'y-shirt_blue_NIKE_M_7000_stripe_.png','y-shirt_white_NIKE_M_7000_dot_.png','y-shirt_white_NIKE_M_7000_stripe_.png']
    check = 0
    best_clothes = 'default'
    my_q = queue.Queue()
    count = 1
    
    while True:
        
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        print("Main")
        if(count == 1):
            faceList = face_pattern.detectMultiScale(gray, 1.5)
            for (x, y, w, h) in faceList:
                cv2.imwrite('./face_original.jpeg', gray[y:y+h, x:x+w])
                print("take a picture")
                count = 2
        

        if check == 0 and count == 2:
            print("tread 1")
            t = threading.Thread(target = Suggest_Color.Suggest_color, args=(frame, count, my_q))
            t.start()   #추천시스템 쓰레드
            check = 1
        img = cv2.flip(frame,1)
        if(count == 1):
            cv2.putText(img,'finding face...',
                    bottomLeftCornerOfText_Title,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (255,0,0),
                    2)
        else:
            cv2.putText(img,'selecting clothes...',
                    bottomLeftCornerOfText_Title,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (255,0,0),
                    2)

        
        cv2.imshow('video', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력시 종료
            break
        if check == 1 and t.isAlive() == False:
            print("thread2")
            t = threading.Thread(target = Suggest_Pattern.Suggest_pattern, args=(frame, count, my_q))
            t.start()   #추천시스템 쓰레드
            check = 2
            
            
            
        if check == 2 and t.isAlive() == False:
            color = my_q.get()
            pattern = my_q.get()
            print(color)   #추천결과
            print(pattern)
            if pattern in "print" :
                pattern = "printing"
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
 

#cap = cv2.VideoCapture(0)
#Third_Menu(cap)
