import cv2
import numpy as np


vid = cv2.VideoCapture(0)
_,instant = vid.read()
avg = np.float32(instant)
obj = 0

upper_pattern = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    _,frame = vid.read()
    cv2.accumulateWeighted(frame, avg, 0.1)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    upperList = upper_pattern.detectMultiScale(gray, 1.5)
    background=cv2.convertScaleAbs(avg)
    diff=cv2.absdiff(frame, background)

    for (x, y, w, h) in upperList:
        cv2.rectangle(frame, (x-w, y+h), (x+2*w, y+4*h), (0, 255, 0), 3)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                 break
    
    cv2.imshow("Upper Body", frame)
    if cv2.waitKey(5)==27:
        break

    
cv2.destroyAllWindows()
