# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:33:01 2021

@author: REYNOLDSPG21
"""

# this code analyzes an image containing four 7x7 ArUco markers on the vertices of a connect four board and having pieces with 4x4 ArUco markers.
# Then produces a matrix containing the piece board locations and team info for each piece


# To Do:
# make this a function like `parse_board_image(...)`

import numpy as np
import time
from miscFunctions import pprintTime

# divide marker codes into groups for human and ai (we've chosen evens&zero vs odds)
HUMAN_CODES = "odds"
AI_CODES = "evensANDzero"


# define array placeholders for marking pieces in board array according to who played the piece
HUMAN_ARRAY_MARKER = 1
AI_ARRAY_MARKER = 2
# by default, empty spaces are zeros (because np.zeros array is created to hold the piece markers)

def get_euler_distance(pt1, pt2):
    return int(((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)**0.5)


# image = cv2.imread('C:/Users/REYNOLDSPG21/OneDrive - Grove City College/Documents/ArUco Codes/test board for coding.png')
image = cv2.imread('C:/Users/REYNOLDSPG21/OneDrive - Grove City College/Documents/ArUco Codes/test board for coding_warped3.png')
# plt.imshow(np.array(image, dtype=np.uint8))

start = time.time()

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
# arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_50"])
boardLinersArucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_7X7_100"])

arucoParams = cv2.aruco.DetectorParameters_create() # if this is too slow, try using passing `useAruco3Detection=True` as an argument (https://docs.opencv.org/4.x/d1/dcd/structcv_1_1aruco_1_1DetectorParameters.html#a5ba4261aa9c097f48e4e64426b16a7e1)

(corners, ids, rejected) = cv2.aruco.detectMarkers(image, boardLinersArucoDict, parameters=arucoParams)

# print(corners[1][0][0][0])

corners = np.array(corners)

############
# do a homographic transform, which conveniently crops the image also
############

# group x coords and y coords together
xvals = np.ones((corners.shape[0], 4))
yvals = np.ones((corners.shape[0], 4))

# sort indices of found codes into x and y arrays
for i in range(0, len(corners)):
    print(i)
    for j in range(0, len(corners[0][0])):
        xvals[i,j] = int(corners[i][0][j][0])
        yvals[i,j] = int(corners[i][0][j][1])


# determine which of each 7x7 code's vertices is closest to the center of the connect four board (so we can crop the image later)
for i in range(0, len(corners)):
    thisCodeavgX = np.average(xvals[i])
    thisCodeavgY = np.average(yvals[i])
    
    if thisCodeavgX>np.average(xvals):
        
        if thisCodeavgY<=np.average(yvals):
            topRightPOI = corners[i][0]
        if thisCodeavgY>np.average(yvals):
            # then bottom right code
            bottomRightPOI = corners[i][0]
		
    if thisCodeavgX<=np.average(xvals):
        if thisCodeavgY<=np.average(yvals):
            # then top left code
            topLeftPOI = corners[i][0]
        if thisCodeavgY>np.average(yvals):
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

start5 = time.time()
# Warp source image to destination based on homography
unwarped_image = cv2.warpPerspective(image, h, (width, height))
pprintTime(start5, time.time())
print("^^ time to just unwarp image")


end = time.time()
pprintTime(start, end)
print("^^ time to locate and process the four boundary codes.\n")

cv2.imshow('asdf', cv2.resize(unwarped_image, (960, 540)))

''' Don't need the below code if we're not using individual ArUco codes on each token...
tokensArucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_100"])

arucoParams = cv2.aruco.DetectorParameters_create() 

(tokensCorners, ids2, rejected2) = cv2.aruco.detectMarkers(unwarped_image, tokensArucoDict, parameters=arucoParams)


# calculate mid-point for each token code
tokenMidPts = np.empty((len(tokensCorners) , 2))
for k in range(0, len(tokensCorners)):
    x = [p[0] for p in tokensCorners[k][0]]
    y = [p[1] for p in tokensCorners[k][0]]
    tokenMidPts[k] = (np.mean(x), np.mean(y))
   
xDim = 7
xBins = np.arange(0, 1, 1/(xDim))
xBins = np.append(xBins, 1)

yDim = 6
yBins = np.arange(0, 1, 1/(yDim))
yBins = np.append(yBins, 1)

board = np.empty((yDim, xDim))


start = time.time()
# now commence binning based on normalized tokenMidPts          
for i in range(0, xDim):
    for j in range(0, yDim):
        for k in range(0, len(tokenMidPts)):
            if (tokenMidPts[k][0]/np.shape(unwarped_image)[1] >= xBins[i]) and (tokenMidPts[k][0]/np.shape(unwarped_image)[1] < xBins[i+1]):
                if (tokenMidPts[k][1]/np.shape(unwarped_image)[0] >= yBins[j]) and (tokenMidPts[k][1]/np.shape(unwarped_image)[0] < yBins[j+1]):
                    # then we've located a piece...
                    if ids2[i] % 2 == 0 or ids2[i] == 0:
                        # the piece is even or zero, so mark array with proper marker
                        if HUMAN_CODES == 'evensANDzero':
                            board[j][i] = HUMAN_ARRAY_MARKER
                        elif AI_CODES == 'evensANDzero':
                            board[j][i] = AI_ARRAY_MARKER
                    elif ids2[i] % 2 == 1:
                        # the piece is odd, so mark array with proper marker
                        if HUMAN_CODES == 'odds':
                            board[j][i] = HUMAN_ARRAY_MARKER
                        elif AI_CODES == 'odds':
                            board[j][i] = AI_ARRAY_MARKER
                    else: print("Code at", j, i, "does not read as an integer! Therefore, piece is not recorded in array!")
                        
                    # board[j][i] +=1 # for future implementation, change this statement to check if token code is even/odd before assigning matrix placeholder
                    print('found yBin for i=', i, 'and j=', j, 'and k=', k)
                    break
                else:
                    pass
            else:
                pass
end = time.time()
pprintTime(start, end)
print("^^ time to locate and record positions of piece codes.\n")

# plt.imshow(board)
cv2.imshow('asdf2', board)
'''
