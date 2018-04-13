import cv2
import numpy as np
import Make_Clothes_Image
import time

def animationleft(firstindex,secondindex,thirdindex,fourthindex,move,frame):
##    clothes0 = 'coat.png'
##    clothes1 = 'hoodT1.png'
##    clothes2 = 'T-shirt.png'
##    clothes3 = 'pants1.png'
##    clothes4 = 'super.png'
    millis_start = int(round(time.time() * 1000))
    clothes = ['t-shirt6_no_DONG_M_7700_.png','hoodT1_no_GUZZI_L_15000_.png','T-shirt_no_PERARI_L_6700_.png','hoodt5_no_NIKE_M_9999_.png','blueshirts_no_WHAT_M_8000_.png']

    y=[int(round(30-3*move)),int(round(30-3*move))+int(round(100-11*move)),int(round(75-5*move)),int(round(75-5*move))+int(round(125-7-2*move)),int(round(30+5*move)),int(round(30+5*move))+int(round(100+7+2*move)),int(round(3+3*move)),int(round(3+3*move))+int(round(10+10*move))]
    x=[int(round(50-5*move)),int(round(50-5*move))+int(round(100-11*move)),int(round(250-20-20*move)),int(round(250-20-20*move))+int(round(150-5-5*move)),int(round(480-23-23*move)),int(round(480-23-23*move))+int(round(100+5+5*move)),int(round(590-11-11*move)),int(round(590-11-11*move))+int(round(10+10*move))]



    Make_Clothes_Image.make_Clothes_Image(clothes[firstindex],(int(round(100-11*move)), int(round(100-11*move))),y[0],y[1],x[0],x[1],frame,clothes[firstindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[secondindex],(int(round(150-5-5*move)),int(round(125-7-2*move))),y[2],y[3],x[2],x[3],frame,clothes[secondindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[thirdindex],(int(round(100+5+5*move)),int(round(100+7+2*move))),y[4],y[5],x[4],x[5],frame,clothes[thirdindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[fourthindex],(int(round(10+10*move)),int(round(10+10*move))),y[6],y[7],x[6],x[7],frame,clothes[fourthindex].split("_")[1][0])

    millis_end = int(round(time.time() * 1000))
    print("AnimationLeftCall : ",millis_end - millis_start,"ms")
    #print(clothes[secondindex])
    return clothes[secondindex]

