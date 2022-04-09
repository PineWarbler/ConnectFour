# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:46:09 2022

@author: REYNOLDSPG21
"""

# all dimensions in mm (just make sure that the units for all measurements are the same)
holeDiameter = 25

middleGapsX = 9.7
sideGapsX = 13.5

topBottomGapsY = 9
middleGapsY = 6.8

def getPixelBins(imagePixelDim, numTokensOnAxis, holeDiameter, middleGap, externalGap):
    '''
    returns integer pixel values of token piece centers in an image of connect four board

    Parameters
    ----------
    imagePixelDim : int
        height or width of the image in pixel units
    numTokensOnAxis : int
        number of tokens along axis (in this case: 6 for y, 7 for x)
    --- make sure that all the following have matching real-life units! ---
    holeDiameter : int/double
        diameter of each hole
    middleGap : int/double
        internal gaps between pieces (excluding the border of the board)
    externalGap : int/double
        extreme gaps between pieces (excluding middle gaps of board)
    totalBoardRealDim : int/double
        real measurement of board

    Returns
    -------
    numpy array
        numpy array containing integer pixel indices


    ---------- NOTE! -------
    -- Recommended arguments: -- 
    holeDiameter = 25

    middleGapsX = 9.7
    sideGapsX = 19.073

    topBottomGapsY = 2.20
    middleGapsY = 6.8

    '''
    import numpy as np

    totalBoardRealDim = (numTokensOnAxis*holeDiameter) + ((numTokensOnAxis-1)*middleGap) + (2*externalGap)

    bins = np.ones(numTokensOnAxis) # make array to fill
    bins[0] = externalGap + (holeDiameter/2) # first token
        
    bins[1:numTokensOnAxis] = (holeDiameter+middleGap) # fill in first edge piece
    return ((np.cumsum(bins)/totalBoardRealDim) * imagePixelDim).astype(int) # normalize to total board dimension and convert to integer pixel values
