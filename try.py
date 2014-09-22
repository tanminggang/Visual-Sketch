import cv2
import numpy as np
import scipy.optimize as so
import pymouse
from PIL import Image
from numpy import *
from pylab import *
import time
#import multiprocessing as mp

FRAME_WIDTH = 200
FRAME_HEIGHT = 200
VIDEO_INTERVAL = 20
cam_index = 0
frame_size = 20

ESC = u'\x1b'

def capture_frames():

    global FRAME_HEIGHT, FRAME_WIDTH, cam_index, frame_size, number        
    cam = cv2.VideoCapture(cam_index)

    red = Image.open("red.jpg")
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

    
def detect_object(frame, red):#480*640

    global VIDEO_INTERVAL, frame_size
         
    x_range = len(frame)
    y_range = len(frame[0])
    
    min_std = 100000000000
    i = 0

    while i <= (y_range - frame_size):
        j = 0
        while j <= (x_range - frame_size):
            std = 0    
            compare_frame = frame[i:i+frame_size, j:j+frame_size, :]
            std = sum(sum(sum(abs(compare_frame - red))))
            if std < min_std:
                min_std = std
                reqx = i
                reqy = j
            j += frame_size
        print min_std
        i += frame_size
        
    cv2.rectangle(frame, (reqx,reqy), (reqx+frame_size,reqy+frame_size), (0,255,0), 2)
    cv2.imshow("Video", frame)
    key = cv2.waitKey(VIDEO_INTERVAL)

def main():
        
    capture_frames()
    
main()
