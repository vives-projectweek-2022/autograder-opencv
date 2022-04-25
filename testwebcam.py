# Python program for Detection of a 
# specific color(blue here) using OpenCV with Python
import cv2
import numpy as np 
  
# Webcamera no 0 is used to capture the frames
cap = cv2.VideoCapture(0) 

#variables for circle blob
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 0
#filter by how Circular the circles are
params.filterByCircularity = True
params.minCircularity = 0.4
#params.
params.filterByConvexity = True
params.minConvexity = 0.2
#threshhold
params.thresholdStep = 5
params.minThreshold = 0
params.maxThreshold = 255

params.filterByInertia = True
params.minInertiaRatio = 0.1

detector = cv2.SimpleBlobDetector_create(params)

# This drives the program into an infinite loop.
while(True):        
    # Captures the live stream frame-by-frame
    _, frame = cap.read() 
    # Converts images from BGR to HSV
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 50, 255, 1)

    rectangle = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle = rectangle[0] if len(rectangle) == 2 else rectangle[1]
  
    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured 
    # objects found in the frame.

  
    # The bitwise and of the frame and mask is done so 
    # that only the blue coloured objects are highlighted 
    # and stored in res

    
    bilateral_filtered_image = cv2.bilateralFilter(frame, 5, 120, 255)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 50, 255)
    keypoints = detector.detect(edge_detected_image)
    blank = np.zeros((1, 1))
    blobs = cv2.drawKeypoints(frame, keypoints, blank, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    cv2.imshow('frame',frame)
    cv2.imshow('mask',edge_detected_image)
  
    # This displays the frame, mask 
    # and res which we created in 3 separate windows.
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
  
# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()
# release the captured frame
cap.release()