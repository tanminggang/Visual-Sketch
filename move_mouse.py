import pymouse
import time
time.sleep(5)
mouse = pymouse.PyMouse()
while(True):
    i = 0
    while( i < 400):
        j = 0
        while(j < 400):
            mouse.move(i, j)
            time.sleep(0.2)
            j += 10
        i += 10
