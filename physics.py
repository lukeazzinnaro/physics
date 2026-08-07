import cv2
import time
import datetime
import numpy as np


cap=cv2.VideoCapture(0)




while True:
    _, frame = cap.read()


    cv2.imshow("Camera",frame)


    grayFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurFrame=cv2.GaussianBlur(grayFrame,(17,17),0)


    circles=cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100, param1=100,param2=30,minRadius=75,maxRadius=400)


    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
