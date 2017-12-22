import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

face_pattern = cv2.CascadeClassifier('Hand.Cascade.1.xml')
count = 0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceList = face_pattern.detectMultiScale(gray, 1.5)
    cv2.rectangle(frame, (450, 50), (600, 200), (255, 0, 0), 3)

    for (x, y, w, h) in faceList:
        if(w>30 & h>10):            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            if((int)((2*x+w)/2)> 450 & (int)((2*x+w)/2) < 600 & (int)((2*y+h)/2) > 50 & (int)((2*y+h)/2) < 200):
                count = count + 1
                print (count)
                if(count>20):
                    cv2.rectangle(frame, (0,0), (100,100),(0,0,255),3)
                    count = 0
                    
                    
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                 break

cap.release()
cv2.destroyAllWindows()    


