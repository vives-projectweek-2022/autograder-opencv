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
        if((w) <= 35 and (w) >= 20 and (h) <= 35 and (h) >= 20):
            cv2.rectangle(ROI, (x, y), (x + w, y + h), (255,50,255), 1)
            Middel = cv2.moments(rect)
            cX = int(Middel["m10"] / Middel["m00"])
            cY = int(Middel["m01"] / Middel["m00"])
            cv2.circle(ROI, (cX, cY), 1, (255, 255, 255), -1)
            cv2.putText(ROI, "centroid" + str(counter), (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
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
    answer = ROI[centerY[0]:centerY[3],centerX[0]:centerX[3]]
    #answer = resize(ROI,centerX,centerY)
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
    return None #out
#circle detecting 

def createRectangle(image):
    MIN_MATCH_COUNT = 10
    img1 = cv.imread(image,0)          # queryImage
    img2 = cv.imread('./img/cropped_sheet.png',0) # trainImage
    # Initiate SIFT detector
    sift = cv.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,M)
        img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)
    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)
    img3 = cv.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    plt.imshow(img3, 'gray'),plt.show()
    return img3

def cirlcedetecting(ROI):
    #variables for circle blob
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 0
    params.maxArea = 120
    #filter by how Circular the circles are
    params.filterByCircularity = True
    params.minCircularity = 0.1
    #convexity
    params.filterByConvexity = True
    params.minConvexity = 0.1
    #threshhold
    params.thresholdStep = 5
    params.minThreshold = 20
    params.maxThreshold = 255
    #shape
    params.filterByInertia = True
    params.minInertiaRatio = 0.1
    #blob detector :D
    detector = cv2.SimpleBlobDetector_create(params)

    #convert frame
    bilateral_filtered_image = cv2.bilateralFilter(ROI, 5, 120, 255)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 50, 255)
    cv2.imshow("bilateral_filtered_image", bilateral_filtered_image)
    cv2.imshow("edge_detected_image", edge_detected_image)
    cv2.waitKey(0)
    #detect circles
    keypoints = detector.detect(edge_detected_image)
    #print(str(keypoints[0].pt[0]))
    #draw around blobs
    blank = np.zeros((1, 1))
    circle = cv2.drawKeypoints(ROI, keypoints, blank, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return circle

def getAnswer():
    return None

img = camera()
area = answerArea(img)
cv2.imshow("area", area)
cv2.waitKey(0)
circles = cirlcedetecting(area)
cv2.imshow("Circular Blobs Only", circles)
#remove results
cv2.waitKey(0)
cv2.destroyAllWindows()