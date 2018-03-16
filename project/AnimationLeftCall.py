import cv2
import numpy as np
import Make_Clothes_Image

def animationleft(firstindex,secondindex,thirdindex,fourthindex,move,frame):
##    clothes0 = 'coat.png'
##    clothes1 = 'hoodT1.png'
##    clothes2 = 'T-shirt.png'
##    clothes3 = 'pants1.png'
##    clothes4 = 'super.png'
    clothes = ['coat_no.png','hoodT1_white.png','T-shirt_no.png','pants1_no.png','super_no.png']

    y=[30-3*move,30-3*move+100-11*move,75-5*move,75-5*move+125-7-2*move,30+5*move,30+5*move+100+7+2*move,3+3*move,3+3*move+10+10*move]
    x=[50-5*move,50-5*move+100-11*move,250-20-20*move,250-20-20*move+150-5-5*move,480-23-23*move,480-23-23*move+100+5+5*move,590-11-11*move,590-11-11*move+10+10*move]



    Make_Clothes_Image.make_Clothes_Image(clothes[firstindex],(100-11*move, 100-11*move),y[0],y[1],x[0],x[1],frame,clothes[firstindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[secondindex],(150-5-5*move,125-7-2*move),y[2],y[3],x[2],x[3],frame,clothes[secondindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[thirdindex],(100+5+5*move,100+7+2*move),y[4],y[5],x[4],x[5],frame,clothes[thirdindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[fourthindex],(10+10*move,10+10*move),y[6],y[7],x[6],x[7],frame,clothes[fourthindex].split("_")[1][0])




