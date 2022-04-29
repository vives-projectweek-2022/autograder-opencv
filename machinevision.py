import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import time


class MachineVision:
    def __init__(self):
        self.__maxVal = 45
        self.__minVal = 19
        self.__area = 0
        self.__cirlces = 0
        self.__blobs = 0

    #camera capture photo
    def camera(self):
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
                if((w) <= self.__maxVal and (w) >= self.__minVal and (h) <= self.__maxVal and (h) >= self.__minVal):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,50,255), 1)
                    if(len(borderbox) != 4):
                        borderbox.append(rect)

            cv2.imshow("camera frame",frame)
            k = cv2.waitKey(5) & 0xFF
            if(k == 27):#and len(borderbox) == 4
                ROI = frame
                return ROI
                
    #area of intrest
    def answerArea(self,ROI):
        image = ROI.copy()
        #variables
        centerX = []
        centerY = []
        #filter
        kernel = np.ones((4,4), np.uint8)
        ROI = cv2.dilate(ROI, kernel, iterations=1)

        gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        canny = cv2.Canny(blurred, 50, 255, 1)
            
        rectangle = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rectangle = rectangle[0] if len(rectangle) == 2 else rectangle[1]

        for rect in rectangle:
            x,y,w,h = cv2.boundingRect(rect)
            if((w) <= self.__maxVal and (w) >= self.__minVal and (h) <= self.__maxVal and (h) >= self.__minVal):
                cv2.rectangle(ROI, (x, y), (x + w, y + h), (255,50,255), 1)
                Middel = cv2.moments(rect)
                cX = int(Middel["m10"] / Middel["m00"])
                cY = int(Middel["m01"] / Middel["m00"])
                cv2.circle(ROI, (cX, cY), 1, (255, 255, 255), -1)

                if(len(centerX) != 4):
                    centerX.append(cX)
                    centerY.append(cY)
        
        #sort small to big
        centerX.sort()
        centerY.sort()
        #show results
        cv2.imshow("Image",ROI)
        cv2.waitKey(0)
        
        self.__area = self.resize(image,centerX,centerY)
        return self.__area

    #WIP
    def resize(self,ROI,centerX,centerY): 
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
        #sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        #out = cv2.filter2D(out, -1, sharpen_kernel)
        #out = cv2.resize(out, (250,600), True)
        return out

    def detect_all_circles(self):
        ROI = self.__area
        output = self.__area.copy()
        gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        # detect circles in the image
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 6,
                                param1=150, param2=12,
                                minRadius=4, maxRadius=14)
        # ensure at least some circles were found

        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 1)
                cv2.rectangle(output, (x , y ), (x , y), (0, 128, 255), 1)
            # show the output image
            cv2.imshow("Detected circles", np.hstack([ROI, output]))
            cv2.waitKey(0)
        else:
            print("Did not detect any circles")
            cv2.destroyAllWindows()
        while(len(circles) != 100):
            cv2.imshow("Detected circles", np.hstack([ROI, output]))
            print("Did not detect all circles " + str(len(circles)))
            cv2.destroyAllWindows()
            self.getResults()
            
        self.__cirlces = np.array(circles)
        
    #circle detecting 
    def blobdetecting(self):
        #dilate image
        image = self.__area
        kernel = np.ones((4,4), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        
        #variables for circle blob
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 20
        params.maxArea = 350
        params.filterByInertia = True
        params.minInertiaRatio = 0.1
        #blob detector :D
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(image)

        #draw around blobs
        blank = np.zeros((1, 1))
        blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        matrixkey = []
        for i in range(0,len(keypoints)):
            matrixkey.append([round(keypoints[i].pt[0]), round(keypoints[i].pt[1])])
        cv2.imshow("blobs", blobs)
        self.__blobs = np.array(matrixkey)

    def getImage(self):
        #get image and area of intrest
        img = self.camera()
        area = self.answerArea(img)

    def getResults(self):
        self.getImage()
        self.detect_all_circles()
        self.blobdetecting()
        
    def getBlobs(self):
        return self.__blobs
    
    def getCirlces(self):
        return self.__cirlces
    
    def showCircles(self,image):
        cv2.imshow()