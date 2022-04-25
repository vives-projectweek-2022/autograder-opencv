import cv2
import numpy as np

#draw function global variables
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255,255,255)
thickness = 1
lineType  = 2

#camera capture photo
def camera():
    #declare variables for camera detection
    cap = cv2.VideoCapture(0)
    borderbox = []
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
            if((w) <= 35 and (w) >= 20 and (h) <= 35 and (h) >= 20):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,50,255), 1)
                cv2.putText(frame, str(len(borderbox)) , (50,50), font, fontScale,fontColor,thickness,lineType)
                if(len(borderbox) != 4):
                    borderbox.append(rect)

        cv2.imshow("camera frame",frame)
        k = cv2.waitKey(5) & 0xFF
        if(k == 27):#and len(borderbox) == 4
            ROI = frame
            return ROI
            
#area of intrest
def answerArea(ROI):
    #variables
    borderX = []
    borderY = []
    #filter
    gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 50, 255, 1)
        
    rectangle = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle = rectangle[0] if len(rectangle) == 2 else rectangle[1]

    for rect in rectangle:
        x,y,w,h = cv2.boundingRect(rect)
        if((w) <= 35 and (w) >= 18 and (h) <= 35 and (h) >= 18):
            cv2.rectangle(ROI, (x, y), (x + w, y + h), (255,50,255), 1)
            Middel = cv2.moments(rect)
            cX = int(Middel["m10"] / Middel["m00"])
            cY = int(Middel["m01"] / Middel["m00"])
            #cv2.circle(ROI, (cX, cY), 5, (255, 255, 255), -1)
            #cv2.putText(ROI, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            if(len(borderX) != 4):
                borderX.append(cX)
                borderY.append(cY)
    
    #sort small to big
    borderX.sort()
    borderY.sort()
    #show results
    cv2.imshow("Image",ROI)
    cv2.waitKey(0)
    answer = ROI[borderY[0]:borderY[3],borderX[0]:borderX[3]]
    cv2.imshow("answer Image",answer)
    return answer 

#circle detecting 
def cirlcedetecting(ROI):
    #variables for circle blob
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = False
    params.minArea = 0
    params.maxArea = 120
    #filter by how Circular the circles are
    params.filterByCircularity = True
    params.minCircularity = 0.2
    #convexity
    params.filterByConvexity = True
    params.minConvexity = 0.1
    #threshhold
    #params.thresholdStep = 5
    #params.minThreshold = 120
    #params.maxThreshold = 255
    #shape
    params.filterByInertia = True
    params.minInertiaRatio = 0.1
    #blob detector :D
    detector = cv2.SimpleBlobDetector_create(params)

    #convert frame
    bilateral_filtered_image = cv2.bilateralFilter(ROI, 5, 120, 255)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 50, 255)
    cv2.imshow("Circular Blobs Only", bilateral_filtered_image)
    cv2.imshow("Circular Blobs Only", edge_detected_image)
    cv2.waitKey(0)
    #detect circles
    keypoints = detector.detect(edge_detected_image)
    #print(str(keypoints[0].pt[0]))
    #draw around blobs
    blank = np.zeros((1, 1))
    circle = cv2.drawKeypoints(ROI, keypoints, blank, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return circle

img = camera()
area = answerArea(img)
cv2.imshow("area", area)
cv2.waitKey(0)
circles = cirlcedetecting(area)
cv2.imshow("Circular Blobs Only", circles)
#remove results
cv2.waitKey(0)
cv2.destroyAllWindows()