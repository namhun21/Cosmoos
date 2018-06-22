import cv2
import sys
import numpy as np
import time
import os
import UI_Start 

os.system("sudo modprobe bcm2835-v4l2")

cap = cv2.VideoCapture(0)
print('width:{0},height:{1}'.format(cap.get(3),cap.get(4)))
cap.set(3,640)
cap.set(4,480)


UI_Start.First_Menu(cap)    #첫번째 화면을 실행한다.


