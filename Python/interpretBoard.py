# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 2022

@author: REYNOLDSPG21
"""

def interpretBoard(image, useBackupThreshes=False, numThreshRed=0, numThreshYellow=0, diagnosticPlot=False):
    '''
    Processes an RGB image of a connect four board surrounded by 4 ArUco fiducial markers and returns an array representation of the piece memberships

    PARAMETERS:
      image : an RGB image of datatype `uint8` with data in the range 0-255
      useBackupThreshes : whether to use backup thresholds for determining piece membership if the camera is having a hard time
        numThreshRed : (only if useBackupThreshes==True) integer between 1 and 2 (inclusive) to select a pre-loaded alternative threshold for red
        numThreshYellow : (only if useBackupThreshes==True) integer between 1 and 2 (inclusive) to select a pre-loaded alternative threshold for yellow
      diagnosticPlot (bool) : whether to plot color thresholds and query locations for the board for troubleshooting
    Returns
    -------
    board : a numpy array of the interpreted board (right side up)
    if some of the four ArUco fiducial markers are not found in the image, function will return None
    '''

    import cv2
    import numpy as np

    # both of the below files are in the GitHub repo
    from getPixelBins import getPixelBins
    from formatImage import formatImage

    if diagnosticPlot==True:
        import matplotlib.pyplot as plt


    formatImage(image, "uint8") # make sure image data is in the 0-255 range

    def get_euler_distance(pt1, pt2):
        return int(((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)**0.5)


    # define names of each possible ArUco tag OpenCV supports
    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    boardLinersArucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_5X5_100"])

    arucoParams = cv2.aruco.DetectorParameters_create()

    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, boardLinersArucoDict, parameters=arucoParams)

    corners = np.array(corners) # turn into numpy array

    # abort the function if we can't find the four codes in the image
    if len(corners) != 4:
        return None

    ############
    # do a homographic transform, which conveniently crops the image also:

    # group x coords and y coords together
    xvals = np.ones((corners.shape[0], 4)) # create empty arrays to fill later
    yvals = np.ones((corners.shape[0], 4))

    for i in range(0, len(corners)):
        for j in range(0, len(corners[0][0])):
            xvals[i,j] = int(corners[i][0][j][0])
            yvals[i,j] = int(corners[i][0][j][1])
            


    yvalAvg = np.average(yvals)
    xvalAvg = np.average(xvals)

    # now group found codes based on their positions in the image (top left, top right, bottom right, bottom left)
    for i in range(0, len(corners)):
        thisCodeavgX = np.average(xvals[i])
        thisCodeavgY = np.average(yvals[i])
        
        if thisCodeavgX>np.average(xvals):
            if thisCodeavgY<=yvalAvg:
                topRightPOI = corners[i][0]
            if thisCodeavgY>yvalAvg:
                # then bottom right code
                bottomRightPOI = corners[i][0]

        if thisCodeavgX<=xvalAvg:
            if thisCodeavgY<=yvalAvg:
                # then top left code
                topLeftPOI = corners[i][0]
            if thisCodeavgY>yvalAvg:
                # then bottom left code
                bottomLeftPOI = corners[i][0]



    # clockwise from top right
    # pt order is top left, top right, bottom right, bottom left
    pts_src = np.array([topLeftPOI[1], topRightPOI[0], bottomRightPOI[3], bottomLeftPOI[2]], dtype=np.float32)

   
    width = get_euler_distance(pts_src[0], pts_src[1])
    height = get_euler_distance(pts_src[0], pts_src[3])

    pts_dst = np.array([[0, 0], [width, 0],  [width, height], [0, height]], dtype=np.float32)


    # Calculate Homography
    h = cv2.getPerspectiveTransform(pts_src, pts_dst)

    # Warp source image to destination based on homography
    unwarped_image = cv2.warpPerspective(image, h, (width, height))

    # ----------------

    numRows = 6
    numCols = 7

    # all dimensions in mm
    holeDiameter = 25

    middleGapsX = 9.7
    sideGapsX = 13.5

    topBottomGapsY = 9
    middleGapsY = 6.8

    # --_--_--_ NEW Hand-Tuned MEASUREMENTS with ArUco holders --_--_--_--_--_
    sideGapsX = (13.5 + 0.573) + 5
    topBottomGapsY = (9 + 0.204) + -7

    # these threshes obtained using PowerToys color picker on example image
    # the tool outputs HSV values (0:360, 0:1, 0:1), but need to convert to:
    # (0:180, 0:255, 0:255) for the cv2.inRange command

    formattingArray = np.array([180/360, 255, 255]) # multiply by raw PowerToys color picker HSV values to properly format for cv2.inRange

    if (useBackupThreshes==False):
        redMinBound = np.array([322, 0.34, 0.53]) * formattingArray
        redMaxBound = np.array([360, 0.99, 0.99]) * formattingArray

        yellowMinBound = np.array([39, 0.17, 0.63]) * formattingArray
        yellowMaxBound = np.array([54, 0.8, 0.99]) * formattingArray

    else:
        backupRedMinBounds = np.array([[339, 0.57, 0.70], [350, 0.80, 0.83], [349, 0.82, 0.84]])
        backupRedMaxBounds = np.array([[353, 0.99, 0.98], [348, 0.97, 0.96], [349, 0.96, 0.97]])

        backupYellowMinBounds=np.array([[39, 0.66, 0.74], [48, 0.74, 0.77], [50, 0.78, 0.81]])
        backupYellowMaxBounds = np.array([[67, 0.98, 0.98], [67, 0.91, 0.91], [61, 0.91, 0.91]])

        redMinBound = backupRedMinBounds[numThreshRed] * formattingArray
        redMaxBound = backupRedMaxBounds[numThreshRed] * formattingArray

        yellowMinBound = backupYellowMinBounds[numThreshYellow] * formattingArray
        yellowMaxBound = backupYellowMaxBounds[numThreshYellow] * formattingArray





    ## convert to hsv
    hsv = cv2.cvtColor(unwarped_image, cv2.COLOR_BGR2HSV)

    if diagnosticPlot==True:
        fig, ax = plt.subplots(nrows=numRows, ncols=numCols)


    board = np.zeros((numRows, numCols))

    centerBinsX = getPixelBins(hsv.shape[1], numCols, holeDiameter, middleGapsX, sideGapsX)
    centerBinsY = getPixelBins(hsv.shape[0], numRows, holeDiameter, topBottomGapsY, middleGapsY)


    pollRadiusRatio = 1 # percent of token's radius to query for token color

    totalBoardRealDimX = (numCols*holeDiameter) + ((numCols-1)*middleGapsX) + (2*sideGapsX)
    averagingRadius = hsv.shape[0]*((holeDiameter/2)/totalBoardRealDimX) * pollRadiusRatio
    averagingRadius = int(averagingRadius)

    thresh = 0.2 # fraction of pixels to qualify as a definite color

    for i in range(0, len(centerBinsX)):
        for j in range(0, len(centerBinsY)):
            window = hsv[int(centerBinsY[j]-averagingRadius) : int(centerBinsY[j]+averagingRadius), int(centerBinsX[i]-averagingRadius) : int(centerBinsX[i]+averagingRadius)]
                       
            yellowMask = cv2.inRange(window, yellowMinBound, yellowMaxBound)
            
            redMask = cv2.inRange(window, redMinBound, redMaxBound) # to display thresholds
            
            if diagnosticPlot==True:
                ax[j, i].imshow(yellowMask + redMask) #row=0, col=0
                cv2.circle(hsv,(centerBinsX[i],centerBinsY[j]), 15, (255,255,255), 5) # overlay circles to indicate query positions on the board

            
            if np.average(yellowMask) > (thresh*255):
                board[j][i] = 1
            elif np.average(redMask) > (thresh*255):
                board[j][i] = 2
            else:
                board[j][i] = 0
    
    if diagnosticPlot==True: 
        plt.show() # show table of windows
        cv2.imshow("Query Locations", hsv)
    
    return board
