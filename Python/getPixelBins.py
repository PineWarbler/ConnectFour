# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:46:09 2022

@author: REYNOLDSPG21
"""

def getPixelBins(imagePixelDim, numTokensOnAxis, holeDiameter, middleGap, externalGap, totalBoardRealDim):
    '''
    returns pixel values of token piece centers in an image of connect four board

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
        containing pixel values along one dimension for centers of tokens

    '''
    bins=np.ones(numTokensOnAxis) # make array to fill
    bins[[0, numTokensOnAxis-1]] = externalGap + (holeDiameter/2) # first and last tokens
        
    bins[1:(numTokensOnAxis-1)] = (holeDiameter+middleGap) # fill in non-edge pieces
    return (np.cumsum(bins)/totalBoardRealDim) * imagePixelDim # normalize to total board dimension and convert to pixel values