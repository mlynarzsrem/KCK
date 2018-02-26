import cv2
import numpy as np
from collections import deque
import argparse
import imutils
from matplotlib import pylab as plt
from pylab import *
from scipy.signal import argrelextrema

def analyze(cord):
    if (len(cord) > 0):
        u = np.mean(cord)
        s = np.std(cord)
        filtered = []
        #Usuwanie outlirerów
        for i in cord:
            if (i <= (u + s)) and (i >= (u - s)):
                filtered.append(i)
        x = np.array(filtered.copy())
        # liczenie podbic
        countMax = x[argrelextrema(x, np.greater)[0]]
        countMin= x[argrelextrema(x, np.less)[0]]
        size = min([len(countMax),len(countMin)])
        if len(countMax)==0 or len(countMin)==0:
            return 0
        diff = []
        for i in range(size):
            diff.append(abs(countMax[i]-countMin[i]))
        u = np.mean(diff)
        s = np.std(diff)
        count = 0
        for i in diff:
            if (i>40):
                count=count +1;
        return count
start =False
cap = cv2.VideoCapture('juggling.mp4')
cord = []
while(cap.isOpened()):
    if cv2.waitKey(33) == ord('a'):
        print("start")
        start=True
    font = cv2.FONT_HERSHEY_SIMPLEX
    if (len(cord) > 0):
        cv2.putText(frame,str(analyze(cord)),(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
    ret, frame = cap.read() #Pobieranie klatki
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Konwersja do czarno białego
    black=gray.copy()
    black[:]=0
    kernel = np.ones((3,3),np.uint8)
    gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    canny=cv2.Canny(gradient,100,300) # Filtr Canny
    #Wykrywanie krawędzi
    im2, contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    outer = []
    for i in range(len(contours)):
        if(hierarchy[0][i][3]==-1 ):#Szukanie zewnętrznych kraędzi
            outer.append(contours[i])
    cv2.drawContours(black, outer, -1, (255, 255, 255), 2) #Rysowanie na czarnym  tle
    cv2.imshow("gray", black)
    #Wykrywanie okręgów
    circles = cv2.HoughCircles(black, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30, minRadius=5, maxRadius=50)
    if circles is not None:
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 1)  # draw the outer circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)  # draw the center of the circle
            if len(circles) == 1 and start==True:
                cord.append(i[1])
            cv2.imshow("Framed", frame)
    else:
        cv2.imshow("Framed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(analyze(cord))
cv2.waitKey(0)
cv2.destroyAllWindows()