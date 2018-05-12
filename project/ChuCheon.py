import queue
import cv2
def ChuCheon(frame, faceList, my_q):
    for (x, y, w, h) in faceList:
            cv2.imwrite('face_original.png', frame[y-70:y+h+20, x-20:x+w+20])
             
            print('finish1')
    total = 0
    for i in range(1, 10000000):
        total += i
    my_q.put(total)
    print('finish2')
