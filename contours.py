#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 00:05:03 2018

@author: abhijithneilabraham
"""

import numpy as np
import cv2


cap = cv2.VideoCapture(0)

while(True):
  # Capture frame-by-frame
   ret, frame = cap.read()

   # Our operations on the frame come here
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   blur = cv2.GaussianBlur(gray,(5,5),0)
   ret, thresh_img = cv2.threshold(blur,91,255,cv2.THRESH_BINARY)
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV(hue saturation value)
   lower_blue = np.array([110,50,50])
   upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
   mask = cv2.inRange(hsv, lower_blue, upper_blue)

   contours =  cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
   
   for c in contours:
       
       cv2.drawContours(frame, [c], -1, (0,255,0), 3)
    
     # Display the resulting frame
   cv2.imshow('frame',frame)
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()