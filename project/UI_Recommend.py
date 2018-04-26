import cv2
import sys
import numpy as np
import time
import os
import UI_Sub
import Function
import overlay
import label_image


def Third_Menu(title,cap):
    bottomLeftCornerOfText_Title = (300,200)
    bodyCascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')

    check = 0
    count = 0
    kinds = title[0]
    if(kinds == 'h'):
        clothes = ['hood-t_black_NIKE_M_9800_.png', 'hood-t_blue_NIKE_M_7000_.png', 'hood-t_gray_NIKE_M_7000_.png', 'hood-t_white_NIKE_M_7000_.png', 'hood-t_beige_NIKE_M_7000_.png']
    elif(kinds == 't'):
        clothes = ['t-shirt_black_ADIDAS_M_8500_.png', 't-shirt_blue_NIKE_M_7000_.png', 't-shirt_gray_NIKE_M_7000_.png', 't-shirt_white_NIKE_M_7000_.png', 't-shirt_beige_NIKE_M_7000_.png']
    else:
        clothes = ['y-shirt_black_GUZZI_M_7500_.png', 'y-shirt_blue_NIKE_M_7000_.png', 'y-shirt_gray_NIKE_M_7000_.png', 'y-shirt_white_NIKE_M_7000_.png', 'y-shirt_beige_NIKE_M_7000_.png']

    while (count<10):
        ret, frame = cap.read()
        img = cv2.flip(frame,1)
        
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        body = bodyCascade.detectMultiScale(
            gray,
            minSize=(100,200),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in body:
            
            if(check == 0):

                cv2.imwrite('original.png',img)

                
                check = check+1
            
                        
        cv2.imshow('video', img)

        if(check == 1):
            cv2.putText(img,'loading```````',
                    bottomLeftCornerOfText_Title,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255,255,255),
                    2)
            
            best_color = label_image.Reco(title,body,clothes)
            count = 10

        if cv2.waitKey(1) & 0xFF == ord('q'):  # q 입력시 종료
            break
    
        

    while True:
        if(best_color == 'black'):
            overlay.Full_Overlay(cap, clothes[0], title)
        elif(best_color == 'blue'):
            overlay.Full_Overlay(cap, clothes[1], title)
        elif(best_color == 'gray'):
            overlay.Full_Overlay(cap, clothes[2], title)
        elif(best_color == 'white'):
            overlay.Full_Overlay(cap, clothes[3], title)
        else:
            overlay.Full_Overlay(cap, clothes[4], title)
        
    cv2.destroyAllWindows()
    cap.release()

#cap = cv2.VideoCapture(0)
#Third_Menu('hood-t', cap)
