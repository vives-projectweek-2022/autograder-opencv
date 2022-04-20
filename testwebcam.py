# Python program for Detection of a 
# specific color(blue here) using OpenCV with Python
import cv2
import numpy as np 
  
# Webcamera no 0 is used to capture the frames
cap = cv2.VideoCapture(2) 

minDist = 100
param1 = 30 #500
param2 = 75 #200 #smaller value-> more false circles
minRadius = 5
maxRadius = 100 #10

# This drives the program into an infinite loop.
while(True):        
    # Captures the live stream frame-by-frame
    _, frame = cap.read() 
    # Converts images from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
  
    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured 
    # objects found in the frame.
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
  
    # The bitwise and of the frame and mask is done so 
    # that only the blue coloured objects are highlighted 
    # and stored in res
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(res, (i[0], i[1]), i[2], (0, 0, 0), 2)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
  
    # This displays the frame, mask 
    # and res which we created in 3 separate windows.
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
  
# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()
# release the captured frame
cap.release()