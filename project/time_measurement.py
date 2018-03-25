import cv2
import numpy as np
import time

def measure(startTime, endTime, sum_time, n):
    
    

    takenTime = endTime - startTime
    sum_time = sum_time + takenTime
    
     
    if(n%10 == 0):
        avg_time = sum_time/10
        sum_time = 0
        print(avg_time)
    n = n+1
    return sum_time,n
    
    
