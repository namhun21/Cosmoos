import cv2
import numpy as np
import Make_Clothes_Image
import time

def animationleft(firstindex,secondindex,thirdindex,fourthindex,move,frame,title):

    #millis_start = int(round(time.time() * 1000))
    kinds = title.split("_")[0][0]
    if(kinds == 'h'):
        clothes = ['hood-t_black_NIKE_M_7000_dot_down.png', 'hood-t_black_NIKE_M_7000_printing_down.png', 'hood-t_blue_NIKE_M_7000_printing_down.png', 'hood-t_gray_NIKE_M_7000_basic_down.png', 'hood-t_white_NIKE_M_7000_basic_down.png']
    elif(kinds == 't'):
        clothes = ['t-shirt_beige_NIKE_M_7000_basic_down.png', 't-shirt_beige_NIKE_M_7000_printing_down.png', 't-shirt_beige_NIKE_M_7000_stripe_down.png', 't-shirt_black_NIKE_M_7000_stripe_down.png', 't-shirt_gray_NIKE_M_7000_dot_down.png','t-shirt_gray_NIKE_M_7000_printing_down.png','t-shirt_gray_NIKE_M_7000_stripe_down.png','t-shirt_white_NIKE_M_7000_printing_down.png']
    else:
        clothes = ['y-shirt_beige_NIKE_M_7000_dot_down.png', 'y-shirt_black_GUZZI_M_7500_basic_down.png', 'y-shirt_blue_NIKE_M_7000_basic_down.png', 'y-shirt_blue_NIKE_M_7000_dot_down.png', 'y-shirt_blue_NIKE_M_7000_stripe_down.png','y-shirt_white_NIKE_M_7000_dot_down.png','y-shirt_white_NIKE_M_7000_stripe_down.png']

    y=[int(round(30-3*move)),int(round(30-3*move))+int(round(100-11*move)),int(round(75-5*move)),int(round(75-5*move))+int(round(125-7-2*move)),int(round(30+5*move)),int(round(30+5*move))+int(round(100+7+2*move)),int(round(3+3*move)),int(round(3+3*move))+int(round(10+10*move))]
    x=[int(round(50-5*move)),int(round(50-5*move))+int(round(100-11*move)),int(round(250-20-20*move)),int(round(250-20-20*move))+int(round(150-5-5*move)),int(round(480-23-23*move)),int(round(480-23-23*move))+int(round(100+5+5*move)),int(round(590-11-11*move)),int(round(590-11-11*move))+int(round(10+10*move))]

    Make_Clothes_Image.make_Clothes_Image(clothes[firstindex],(int(round(100-11*move)), int(round(100-11*move))),y[0],y[1],x[0],x[1],frame)
    Make_Clothes_Image.make_Clothes_Image(clothes[secondindex],(int(round(150-5-5*move)),int(round(125-7-2*move))),y[2],y[3],x[2],x[3],frame)
    Make_Clothes_Image.make_Clothes_Image(clothes[thirdindex],(int(round(100+5+5*move)),int(round(100+7+2*move))),y[4],y[5],x[4],x[5],frame)
    Make_Clothes_Image.make_Clothes_Image(clothes[fourthindex],(int(round(10+10*move)),int(round(10+10*move))),y[6],y[7],x[6],x[7],frame)

    #millis_end = int(round(time.time() * 1000))
    #print("AnimationLeftCall : ",millis_end - millis_start,"ms")
    #print(clothes[secondindex])
    return secondindex
