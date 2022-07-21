# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 14:28:50 2022

@author: P. Reynolds
"""

# refactoring entire window script as a function doesn't work because window is not persistent
# however, calling `exec(open('C:/Users/pgr/Documents/PyQtGraph Dashboard.py').read())` and then `update_dashboard()`
# from another script works just fine
# (see https://stackoverflow.com/a/1186818)

# on on `exec(open...)` call, dashboard will open to default (blank) data
# call update_dashboard(...) to display data


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
import time

col_choice = 5

pg.setConfigOptions(imageAxisOrder='row-major')

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsLayoutWidget(show=True, title="Connect Four Dashboard")
win.resize(1920,1080)
win.setWindowTitle('Data Dashboard')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


# Display Computer Col Choice
choiceAnnouncePlot = win.addPlot(colspan=3)
choiceAnnouncePlot.setTitle("Computer chooses column #NA", color="m", size="30pt")
choiceAnnouncePlot.showAxis('bottom', False) # don't show axes
choiceAnnouncePlot.showAxis('left', False)
choiceAnnouncePlot.setMaximumHeight(150)


win.nextRow()



board_row = plt.imread("C:/Users/pgr/Downloads/board_row_green.JPG")
board_height, board_width = board_row.shape[0:2] # slicing to omit channel (unnecessary)

# board_row = np.rot90(board_row, k=3)
boardRowPlot = win.addPlot(colspan=3)
board_row_item = pg.ImageItem(image=board_row)
boardRowPlot.addItem(board_row_item)
boardRowPlot.setMouseEnabled(x=False, y=False) # disable image zooming
boardRowPlot.showAxis('bottom', False) # don't show axes
boardRowPlot.showAxis('left', False)
boardRowPlot.setAspectLocked(True)

slotRadius = 88 # pixel measurement
# # try placing an arrow on the board_row image instead...
k=2.5 # arrow scaling factor
arrow_symbol = pg.ArrowItem(angle=-90, tipAngle=60, headLen=40*k, tailLen=40*k, tailWidth=20*k, pen=None, brush='m')
# arrow_symbol.setPos(board_width * (0/7) + slotRadius, board_height * 0.8) # (x,y)
# boardRowPlot.addItem(arrow_symbol)



win.nextRow()

# display recursion count
recursionCountText = win.addPlot(colspan=2)
recursionCountText.setTitle(title="<b>" + str(0) + "</b> algorithm recursions executed", size="20pt", color="g")
recursionCountText.showAxis('bottom', False) # don't show axes
recursionCountText.showAxis('left', False)
recursionCountText.setMaximumHeight(100)

# display search depth
searchDepthText = win.addPlot(colspan=1)
searchDepthText.setTitle(title="Search Depth: <b>" + str(0) + "</b>", size="20pt", color="r")
searchDepthText.showAxis('bottom', False) # don't show axes
searchDepthText.showAxis('left', False)
searchDepthText.setMaximumHeight(100)

win.nextRow()


lowestRowMaxHeight = 300
thinkTimesPlot = win.addPlot(title="Think Times")
thinkTimesPlot.plot([], pen=pg.mkPen(color="m", width=5))
thinkTimesPlot.plot([], pen=pg.mkPen(color="b", width=5))
thinkTimesPlot.setLabel('left', "time", units="s")
thinkTimesPlot.setLabel('bottom', "turn #")
thinkTimesPlot.setMaximumHeight(lowestRowMaxHeight)

minimaxScoresPlot = win.addPlot(title="Minimax Scores")
minimaxScoresPlot.plot([], pen=pg.mkPen(color="c", width=5))
minimaxScoresPlot.setLabel('left', "score")
minimaxScoresPlot.setLabel('bottom', "turn #")
minimaxScoresPlot.setMaximumHeight(lowestRowMaxHeight)

threshedImagePlot = win.addPlot(title="Thresholded Image")
# image = plt.imread("D:/Connect4Board.jpg")
image = np.eye(200)
imgItem = pg.ImageItem(image = np.rot90(image)) # the slicing is to rotate by 90 degrees
threshedImagePlot.addItem(imgItem, title="Simplest possible image example") 
threshedImagePlot.showAxis('bottom', False) # don't show axes
threshedImagePlot.showAxis('left', False)
threshedImagePlot.setAspectLocked(True)
threshedImagePlot.setMaximumHeight(lowestRowMaxHeight)

win.showMaximized() # maximize the window



def update_dashboard(col_choice, recursionCount, depth, playerThinkTimes, AIThinkTimes, minimaxScores, threshedImage):
    
    # note that all font styling has already been set by the main program
    # plot styles need to be repeated in this function, though
    
    
    # announce column choice
    choiceAnnouncePlot.setTitle("Computer chooses column #<b>" + str(col_choice) + "</b>")
    
    
    # arrow symbol
    arrow_symbol.setPos(board_width * (col_choice/7) + slotRadius, board_height * 0.8) # (x,y)
    boardRowPlot.addItem(arrow_symbol)
    
    # display recursion count
    recursionCountText.setTitle(title="<b>" + str(recursionCount) + "</b> algorithm recursions executed")
    
    # display search depth
    searchDepthText.setTitle(title="Search Depth: <b>" + str(depth) + "</b>")
    
    # plot think times
    thinkTimesPlot.addLegend()
    thinkTimesPlot.plot(AIThinkTimes, pen=pg.mkPen(color="m", width=5), name="Computer")
    thinkTimesPlot.plot(playerThinkTimes, pen=pg.mkPen(color="b", width=5), name="You")
    
    # plot minimax scores
    minimaxScoresPlot.plot(minimaxScores, pen=pg.mkPen(color="c", width=5))
    
    # display threshed image
    imgItem = pg.ImageItem(image = threshedImage)
    threshedImagePlot.addItem(imgItem) 
    
    app.processEvents()
