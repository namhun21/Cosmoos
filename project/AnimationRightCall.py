import cv2
import numpy as np
import Make_Clothes_Image
import time

def animationright(firstindex,secondindex,thirdindex,fourthindex,move,frame,title):

    millis_start = int(round(time.time() * 1000))
    kinds = title.split("_")[0][0]
    if(kinds == 'h'):
        clothes = ['hood-t_black_NIKE_M_9800_down.png', 'hood-t_blue_NIKE_M_7000_down.png', 'hood-t_red_NIKE_M_7000_down.png', 'hood-t_white_NIKE_M_7000_down.png', 'hood-t_yellow_NIKE_M_7000_down.png']
    elif(kinds == 't'):
        clothes = ['t-shirt_black_ADIDAS_M_8500_down.png', 't-shirt_blue_NIKE_M_7000_down.png', 't-shirt_red_NIKE_M_7000_down.png', 't-shirt_white_NIKE_M_7000_down.png', 't-shirt_yellow_NIKE_M_7000_down.png']
    else:
        clothes = ['y-shirt_black_GUZZI_M_7500_down.png', 'y-shirt_blue_NIKE_M_7000_down.png', 'y-shirt_red_NIKE_M_7000_down.png', 'y-shirt_white_NIKE_M_7000_down.png', 'y-shirt_yellow_NIKE_M_7000_down.png']


    y=[int(round(3+3*move)),int(round(3+3*move))+int(round(10+10*move)),int(round(30+5*move)),int(round(30+5*move))+int(round(100+7+2*move)),int(round(75-5*move)),int(round(75-5*move))+int(round(125-7-2*move)),int(round(30-3*move)),int(round(30-3*move))+int(round(100-11*move))]
    x=[int(round(5+5*move)),int(round(5+5*move))+int(round(10+10*move)),int(round(50+20+20*move)),int(round(50+20+20*move))+int(round(100+5+5*move)),int(round(250+23+23*move)),int(round(250+23+23*move)) + int(round(150-5*move)),int(round(480+12+12*move)),int(round(480+12+12*move))+int(round(100-11*move))]


    Make_Clothes_Image.make_Clothes_Image(clothes[firstindex],(int(round(10+10*move)), int(round(10+10*move))),y[0],y[1],x[0],x[1],frame)
    Make_Clothes_Image.make_Clothes_Image(clothes[secondindex],(int(round(100+5+5*move)),int(round(100+7+2*move))),y[2],y[3],x[2],x[3],frame)
    Make_Clothes_Image.make_Clothes_Image(clothes[thirdindex],(int(round(150-5*move)),int(round(125-7-2*move))),y[4],y[5],x[4],x[5],frame)
    Make_Clothes_Image.make_Clothes_Image(clothes[fourthindex],(int(round(100-11*move)),int(round(100-11*move))),y[6],y[7],x[6],x[7],frame)

    print(clothes[thirdindex])
    millis_end = int(round(time.time() * 1000))
    print("AnimationRightCall : ",millis_end - millis_start,"ms")
    return thirdindex

