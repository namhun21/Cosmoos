import cv2
import numpy as np
import time

def measure_UI_Start(startTime, endTime, sum_time, n):
    

    takenTime = endTime - startTime
    sum_time = sum_time + takenTime
    
     
    if(n%10 == 0):
        avg_time = sum_time/10
        sum_time = 0
        print("UI_Start time: ",avg_time)
    n = n+1
    return sum_time,n
    
    
def measure_UI_Sub(startTime, endTime, sum_time, n):
    

    takenTime = endTime - startTime
    sum_time = sum_time + takenTime
    
     
    if(n%10 == 0):
        avg_time = sum_time/10
        sum_time = 0
        print("UI_Sub: ",avg_time)
    n = n+1
    return sum_time,n

def measure_SelectClothes(startTime, endTime, sum_time, n):
    

    takenTime = endTime - startTime
    sum_time = sum_time + takenTime
    
     
    if(n%10 == 0):
        avg_time = sum_time/10
        sum_time = 0
        print("SelectClothes: ",avg_time)
    n = n+1
    return sum_time,n

def measure_Click_Function(startTime, endTime, sum_time, n):
    

    takenTime = endTime - startTime
    sum_time = sum_time + takenTime
    
     
    if(n%10 == 0):
        avg_time = sum_time/10
        sum_time = 0
        print("Click_Function: ",avg_time)
    n = n+1
    return sum_time,n

