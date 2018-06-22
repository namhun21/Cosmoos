import cv2
import os
import time

#차재성 학생이 작성하였습니다.
#텐서플로우 작업을 하는데 있어서 필요한 작업입니다.
def crop_image(color):
    select_color = os.listdir('./{}'.format(color))
    print(select_color)
    face_pattern = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')
    i = 0
    while i < len(select_color):
        #time.sleep(1)
        image = cv2.imread('./{0}/{1}'.format(color,select_color[i]))
        # image = cv2.imread('1702.jpg')
        time.sleep(0.5)
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        face = face_pattern.detectMultiScale(image,scaleFactor=1.1, minNeighbors=1, minSize=(40, 40))
        print(select_color[i])

        if len(face) == 0:
            print("No Face")
            i = i+1
            continue
    # print(face)
    # cv2.imshow('image', image)
    # cv2.waitKey(0)


        print("OK!",select_color[i])
        for (x, y, w, h) in face:
            print(face)
            if y < 100:
                image_crop = image[y:(y+h),x:(x+w)]
                image_crop = cv2.resize(image_crop, (w*5, h*5))
                cv2.imwrite('./{0}/Crop_{1}'.format(color, select_color[i]), image_crop)
                shrink = cv2.resize(image_crop, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                shrink = cv2.resize(shrink, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
                cv2.imwrite('./{0}/Crop_shrink{1}'.format(color,select_color[i]), shrink)
        i = i + 1

crop_image('basic')
crop_image('dot')
crop_image('print')
crop_image('stripe')
#crop_image('white')


