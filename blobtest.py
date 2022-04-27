import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

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
            if((w) <= 35 and (w) >= 10 and (h) <= 35 and (h) >= 10):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,50,255), 1)
                #cv2.putText(frame, str(len(borderbox)) , (50,50), font, fontScale,fontColor,thickness,lineType)
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
    centerX = []
    centerY = []
    counter = 0
    #filter
    gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 50, 255, 1)
        
    rectangle = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle = rectangle[0] if len(rectangle) == 2 else rectangle[1]

    for rect in rectangle:
        x,y,w,h = cv2.boundingRect(rect)
        if((w) <= 35 and (w) >= 12 and (h) <= 35 and (h) >= 12):
            cv2.rectangle(ROI, (x, y), (x + w, y + h), (255,50,255), 1)
            Middel = cv2.moments(rect)
            cX = int(Middel["m10"] / Middel["m00"])
            cY = int(Middel["m01"] / Middel["m00"])
            cv2.circle(ROI, (cX, cY), 1, (255, 255, 255), -1)
            #cv2.putText(ROI, "centroid" + str(counter), (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            counter += 1
            if(len(centerX) != 4):
                centerX.append(cX)
                centerY.append(cY)
    
    #sort small to big
    centerX.sort()
    centerY.sort()
    for i in range(len(centerX)):
        print("X"+ str(i) +" :" + str(centerX[i]))
        print("Y"+ str(i) +" :" + str(centerY[i]))
    #show results
    cv2.imshow("Image",ROI)
    cv2.waitKey(0)
    
    answer = resize(ROI,centerX,centerY)
    return answer 

def resize(ROI,centerX,centerY): 
    #pt_A = [centerX[0],centerY[0]]
    #pt_B = [centerX[1],centerY[1]]
    #pt_C = [centerX[2],centerY[2]]
    #pt_D = [centerX[3],centerY[3]]
    
    # Here, I have used L2 norm. You can use L1 also.
    #width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
    #width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
    #maxWidth = max(int(width_AD), int(width_BC))


    #height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
    #height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
    #maxHeight = max(int(height_AB), int(height_CD))
    # Apply Perspective Transform Algorithm
    #input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
    #output_pts = np.float32([[0, 0],
                            #[0, maxHeight - 1],
                            #[maxWidth - 1, maxHeight - 1],
                            #[maxWidth - 1, 0]])
    # Compute the perspective transform M
    #M = cv2.getPerspectiveTransform(input_pts,output_pts)
    #out = cv2.warpPerspective(img,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)
    
    out = ROI[centerY[0]:centerY[3],centerX[0]:centerX[3]]
    out = cv2.resize(out, (1000,500), interpolation= cv2.INTER_LINEAR)
    return out
#circle detecting 
def cirlcedetecting(image):
    #variables for circle blob
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 60
    params.maxArea = 300
    #filter by how Circular the circles are
    params.filterByCircularity = True
    params.minCircularity = 0.1
    #convexity
    params.filterByConvexity = True
    params.minConvexity = 0.4
    #threshhold
    #params.thresholdStep = 5
    params.minThreshold = 5
    params.maxThreshold = 255
    #shape
    params.filterByInertia = True
    params.minInertiaRatio = 0.01
    #blob detector :D
    detector = cv2.SimpleBlobDetector_create(params)

    #convert frame
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray blobs",gray)
    cv2.waitKey(0)
    #detect circles
    keypoints = detector.detect(gray)
    #print(str(keypoints[0].pt[0]))
    #draw around blobs
    blank = np.zeros((1, 1))
    circle = cv2.drawKeypoints(image, keypoints, blank, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return circle

def getAnswer():
    return None

img = camera()
area = answerArea(img)
circles = cirlcedetecting(area)
cv2.imshow("blobs", circles)
#remove results
cv2.waitKey(0)
cv2.destroyAllWindows()