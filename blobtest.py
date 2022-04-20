from unittest import skip
import cv2
import numpy as np
import keyboard

#read image
cap = cv2.VideoCapture(0) 
#correct answers
correctAnswer = [2,4]
circles = []
amount = 0
border = []
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
        if((x+w)-x <= 25 and (x+w)-x >= 10 and (y+h)- y <= 25 and (y+h)- y >= 10):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255,50,0), 1)
            

    cv2.imshow("only black box",canny)    
    cv2.imshow("Original Image",frame)
    k = cv2.waitKey(5) & 0xFF
    if(k == 27 and len(rectangle) == 4):
        ROI = frame
        break

gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
canny = cv2.Canny(blurred, 50, 255, 1)
    
rectangle = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
rectangle = rectangle[0] if len(rectangle) == 2 else rectangle[1]

for rect in rectangle:
    x,y,w,h = cv2.boundingRect(rect)
    if((x+w)-x <= 25 and (x+w)-x >= 10 and (y+h)- y <= 25 and (y+h)- y >= 10):
        cv2.rectangle(ROI, (x, y), (x + w, y + h), (0,50,255), 1)
        if(len(border) != 8):
                border.append(x)
                border.append(y)

for i in range(0,len(border)):
    print(border[i])
cv2.putText(ROI, '1' , (border[0],border[1]), font, fontScale,fontColor,thickness,lineType)
cv2.putText(ROI, '2' , (border[2],border[3]), font, fontScale,fontColor,thickness,lineType)
cv2.putText(ROI, '3' , (border[4],border[5]), font, fontScale,fontColor,thickness,lineType)
cv2.putText(ROI, '4' , (border[6],border[7]), font, fontScale,fontColor,thickness,lineType)

#show results

cv2.imshow("new Image",ROI)
cv2.waitKey(0)
img = ROI[border[5]:border[4],border[3]:border[2]]
cv2.imshow("new Image",img) 
#cv2.imshow("Circular Blobs Only", blobs)
#remove results
cv2.waitKey(0)
cv2.destroyAllWindows()