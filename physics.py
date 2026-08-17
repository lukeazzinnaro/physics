import cv2
import time
import datetime
import numpy as np
from math import *


cap=cv2.VideoCapture(0)
prevCircle=None
dist = lambda x1,y1,x2,y2: sqrt(((x1-x2)**2 + (y1-y2)**2))
Starttime=time.time()
speed_conversion=.02/91
speeds=[]
accelerations=[]


while True:
    _, frame = cap.read()


   
    grayFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurFrame=cv2.GaussianBlur(grayFrame,(17,17),0)
   


    circles=cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.35, 100, param1=110,param2=27,minRadius=70,maxRadius=80)
    if circles is not None:
        circles=np.round(circles).astype(int)
        chosen=None
        for i in circles[0,:]:
                        mask=np.zeros(frame.shape[:2],dtype=np.uint8)
            cv2.circle(mask,(i[0],i[1]),i[2],255,-1)
            hsvFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            meanColor=cv2.mean(hsvFrame,mask=mask)

            if not (5 <= meanColor[0] <= 25 and meanColor[1] > 80):
                continue
            if chosen is None: chosen=i
            if prevCircle is None:
                prevCircle=chosen
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) >= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                    chosen=i
        cv2.circle(frame, (chosen[0], chosen[1]),1,(0,100,0),3)
        cv2.circle(frame, (chosen[0], chosen[1]),chosen[2],(255,0,0),2)
        cv2.line(frame,(int(prevCircle[0]), int(prevCircle[1])),(int(chosen[0]), int(chosen[1])),(0, 255, 0),2)
        elapsedtime=time.time()-Starttime
        Starttime=time.time()
        speed=dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1])/elapsedtime
        m_s_speed=speed*speed_conversion
        speeds.append(m_s_speed)
        if len(speeds)>10:
            del speeds[0:5]
        average_speed=sum(speeds)/len(speeds)
        prevCircle=chosen
        acceleration=average_speed/elapsedtime
        accelerations.append(acceleration)
        if len(accelerations)>10:
            del accelerations[0:5]
        average_acceleration=sum(accelerations)/len(accelerations)


       


        cv2.putText(frame,f'R: {chosen[2]}', (chosen[0]+100,chosen[1]), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.putText(frame,f'Speed (m/s): {round(float(average_speed),2)})', (35,35), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        cv2.putText(frame,f'Acceleration (m/s^2): {round(float(average_acceleration),2)})', (35,75), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        cv2.imshow("circles",frame)


    if cv2.waitKey(1) == ord('q'):
        break


print(chosen[2])
cap.release()
cv2.destroyAllWindows()


