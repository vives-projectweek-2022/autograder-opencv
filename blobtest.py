import cv2
import numpy as np
import keyboard

#read image
cap = cv2.VideoCapture(0) 
#correct answers
correctAnswer = [2,4]
circles = []
amount = 0
count = 0
#variables for circle blob
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 300
#filter by how Circular the circles are
params.filterByCircularity = True
params.minCircularity = 0.4
#convexity
params.filterByConvexity = True
params.minConvexity = 0.2
#threshhold
params.thresholdStep = 5
params.minThreshold = 200
params.maxThreshold = 255
#shape
params.filterByInertia = True
params.minInertiaRatio = 0.1
#blob detector :D
detector = cv2.SimpleBlobDetector_create(params)

#variables rectangles
counter = 0
parts = []
areas = []

#draw
font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2

while(True):
    _, frame = cap.read() 
    #draw detected rectangles
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 50, 255, 1)
    
    rectangle = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle = rectangle[0] if len(rectangle) == 2 else rectangle[1]

    for rect in rectangle:
        x,y,w,h = cv2.boundingRect(rect)
        if((x+w)-x <= 25 and (y+h)- y <= 25):
            text = str(count) + " rect"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255,50,0), 1)
            if(count < 4):
                cv2.putText(frame, text , (x,y), font, fontScale,fontColor,thickness,lineType)
                count += 1

    cv2.imshow("only black box",canny)    
    cv2.imshow("Original Image",frame)
    if(len(rectangle) == 4 and keyboard.is_pressed('q')):
        ROI = frame
        cv2.imshow("Original Image",ROI)
        cv2.waitKey(0)
        break
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


#show results    
cv2.imshow("Original Image",ROI)
#cv2.imshow("Circular Blobs Only", blobs)
#remove results
cv2.waitKey(0)
cv2.destroyAllWindows()