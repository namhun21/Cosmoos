import numpy as np
import cv2
import time
import time_measurement
import os
sum_time = 0
n = 0
os.system("sudo modprobe bcm2835-v4l2")
capture = cv2.VideoCapture(0)

capture.set(3, 320)
capture.set(4, 240)


while True:
    First_Menu_startTime = int(round(time.time() * 1000))
    ret, frame = capture.read()

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    First_Menu_endTime = int(round(time.time() * 1000))

    sum_time, n = time_measurement.measure(First_Menu_startTime, First_Menu_endTime, sum_time, n)

capture.release()
cv2.destroyAllWindows()