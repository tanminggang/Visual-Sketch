import cv2
import numpy as np
import scipy.optimize as so
import pymouse
from PIL import Image
from numpy import *
from pylab import *
import time
import math

#green = np.uint8([[[0,255,0 ]]])
#hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
#take [H-10, 100,100] and [H+10, 255, 255]
#import multiprocessing as mp

FRAME_WIDTH = 200
FRAME_HEIGHT = 200
VIDEO_INTERVAL = 20
cam_index = 0
frame_size = 20

ESC = u'\x1b'
BASE_TIME = time.time()
INIT = False
mouse = pymouse.PyMouse()
screen_width, screen_height = mouse.screen_size()

def capture_frames():

    global FRAME_HEIGHT, FRAME_WIDTH, cam_index, frame_size, number, BASE_TIME
            
    cam = cv2.VideoCapture(cam_index)

    red = Image.open("new.jpg")
    red = red.resize((frame_size,frame_size), Image.ANTIALIAS)   
    red = array(red)

    while True:
    # video capture
        ret, frame = cam.read()
        
        if frame is None:
            continue
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame = cv2.flip(frame, 1)
        detect_object(frame, red)     
        key = cv2.waitKey(VIDEO_INTERVAL)
        if key == ESC:
            break       
        elapsed_time = int(time.time() - BASE_TIME)
        if elapsed_time >= 30:
            break
            
def moveMouse(x, y):

    global BASE_TIME, mouse, INIT, screen_width, screen_height
    print x,y
    x = x * ((screen_width + 0.0) / FRAME_WIDTH)
    y = y * ((screen_height + 0.0) / FRAME_HEIGHT)
    
    x = round(x)
    y = round(y)    
#    x = x * 3
#    y = y * 3
#    elapsed_time = (datetime.now() - BASE_TIME).seconds
#    if elapsed_time > 0.5:
    INIT = True
    mouse.move(x, y)
    mouse.click(x,y)
    mouse.press(x, y)
#    BASE_TIME = elapsed_time
#    mouse.release(x, y)            

def detect_object(frame, red):#480*640

    global VIDEO_INTERVAL, frame_size
         
    x_range = len(frame)
    y_range = len(frame[0])
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #range
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    white = np.zeros(shape=(frame_size, frame_size))
    white += 255
    
    min_std = 100000000000
    i = 0
    temp = frame
    frame = mask
    while i <= (y_range - frame_size):
        j = 0
        while j <= (x_range - frame_size):
            std = 0    
            compare_frame = frame[i:i+frame_size, j:j+frame_size]
            std = math.sqrt(sum(sum(sum(abs(compare_frame - white)))))
            if std < min_std:
                min_std = std
                reqx = i
                reqy = j 
            j += frame_size
        i += frame_size
    
    frame = temp
    cv2.rectangle(frame, (reqy,reqx), (reqy+frame_size,reqx+frame_size), (0,255,0), 2)
    cv2.imshow("Video", frame)
    key = cv2.waitKey(VIDEO_INTERVAL)
    if INIT is False:
        print "waiting now"
        time.sleep(15)
    moveMouse((reqy + frame_size) / 2.0, (reqx + frame_size) / 2.0)
    
def main():
        
    capture_frames()
    
main()
