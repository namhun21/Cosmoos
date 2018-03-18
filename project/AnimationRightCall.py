import cv2
import numpy as np
import Make_Clothes_Image
def animationright(firstindex,secondindex,thirdindex,fourthindex,move,frame):
##    clothes0 = 'coat_no.png'
##    clothes1 = 'hoodT1_white.png'
##    clothes2 = 'T-shirt_no.png'
##    clothes3 = 'pants1_no.png'
##    clothes4 = 'super_no.png'
    clothes = ['coat_no.png','hoodT1_white.png','T-shirt_no.png','pants1_no.png','super_no.png']



    y=[3+3*move,3+3*move+10+10*move,30+5*move,30+5*move+100+7+2*move,75-5*move,75-5*move+125-7-2*move,30-3*move,30-3*move+100-11*move]
    x=[5+5*move,5+5*move+10+10*move,50+20+20*move,50+20+20*move+100+5+5*move,250+23+23*move,250+23+23*move + 150-5*move,480+12+12*move,480+12+12*move+100-11*move]


    Make_Clothes_Image.make_Clothes_Image(clothes[firstindex],(10+10*move, 10+10*move),y[0],y[1],x[0],x[1],frame,clothes[firstindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[secondindex],(100+5+5*move,100+7+2*move),y[2],y[3],x[2],x[3],frame,clothes[secondindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[thirdindex],(150-5*move,125-7-2*move),y[4],y[5],x[4],x[5],frame,clothes[thirdindex].split("_")[1][0])
    Make_Clothes_Image.make_Clothes_Image(clothes[fourthindex],(100-11*move,100-11*move),y[6],y[7],x[6],x[7],frame,clothes[fourthindex].split("_")[1][0])

    print(clothes[thirdindex])
    return clothes[thirdindex]

