import cv2
import numpy as np 
from math import sqrt
import RPi.GPIO as GPIO
from time import sleep
cap=cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
turn_threshold_1=80
turn_threshold_2=50
turn_threshold_3=20
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
Motor1E = 22
 
Motor2A = 23
Motor2B = 21
Motor2E = 19

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
 
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

def find_contour(frame,x,y):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([-10,50,50])
    upper = np.array([8,255,255])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskFinal=maskClose
    _,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if len(conts)!=0:    
        c=max(conts,key=cv2.contourArea)
        cv2.drawContours(frame,c,-1,(0,0,0),3)
        m=cv2.moments(c)
        cx=int(m["m10"]/m["m00"])
        #cy=int(m["m01"]/m["m00"])
        cv2.circle(frame,(cx,y),7,(255,0,0),2)
        dist=cx-x
        return dist
    return None
def turnright():
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
def turnleft():
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
def set_speed(v):
    global speed
    if v==1:
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
 
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)
        speed=1
    elif v==0:
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.LOW)
 
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        speed=0
        
def thrustercontrol(x1,x2,x3):
    if x1==x2==x3==None:
        set_speed(0)
    elif x1!=None or x2!=None or x3!=None and speed==0:
        set_speed(1)
    if x2>turn_threshold_2:
        turnright()
    elif x2<-(turn_threshold_2):
        turnleft()
while True:
    _,frame=cap.read()
    res=cv2.resize(frame,(320,240))
    slices=[res[0:80,0:320],res[80:160,0:320],res[160:240,0:320]]
    cv2.circle(res,(160,40),7,(0,100,100),2)
    cv2.circle(res,(160,120),7,(0,100,100),2)
    cv2.circle(res,(160,200),7,(0,100,100),2)
    d1=find_contour(slices[0],160,40)
    d2=find_contour(slices[1],160,40)
    d3=find_contour(slices[2],160,40)
    #res[0:80,0:320]=[255,255,255]
    cv2.imshow("frame",res)
    print(d1,d2,d3)
    
    
    cv2.waitKey(1)   

