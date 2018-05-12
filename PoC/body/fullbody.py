import cv2
import numpy as np


vid = cv2.VideoCapture(0)


face_pattern = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
check = 0
count = 0

while True:
    ret,frame = vid.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faceList = face_pattern.detectMultiScale(gray, 1.5)

    for (x, y, w, h) in faceList:
        cv2.rectangle(frame, (x-20, y-70), (x+w+20, y+h+20), (0, 255, 0), 3)
        if(count == 10):
            cv2.imwrite('face_original.png', frame[y-70:y+h+20, x-20:x+w+20])

    
    img = cv2.flip(frame,1)

    cv2.imshow("Face", img)

    
    count = count + 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
cv2.destroyAllWindows()
