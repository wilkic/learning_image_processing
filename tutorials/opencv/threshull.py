
# Same as 'clear all'
from IPython import get_ipython
ipython = get_ipython()
ipython.magic('reset -f')

###############################################

import numpy as np
import cv2
from openalpr import Alpr

import time
import sys
sys.path.append('..')
import notifications as notify

from matplotlib import pyplot as plt

###############################################

# Contour area above which, a car is registered
Slim = 80e3

###############################################

call = "ffmpeg -rtsp_transport tcp -r 25 -y -i rtsp://108.45.109.111:9209/live0.264 -updatefirst 1 -r 2 cam09.bmp"

###############################################

# Load the baseline image
bfilename = '../minicatch/cam09_bg.bmp'
bim = cv2.imread(bfilename)
bimgray = cv2.cvtColor(bim, cv2.COLOR_BGR2GRAY)
bimhsv = cv2.cvtColor(bim, cv2.COLOR_BGR2HSV)

#fname = 'cam09_24_26.bmp'
fname = '../minicatch/cam09_new25.bmp'
#fname = 'cam09.bmp'
#fname = '/home/acp/work/camera_testing/hosafe/cam9/just_lx.bmp'
#fname = '/home/acp/work/camera_testing/hosafe/cam9/lx.bmp'
#fname = '/home/acp/work/camera_testing/hosafe/cam9/tess.bmp'
#fname = '/home/acp/work/camera_testing/hosafe/cam9/bg.bmp'

im = cv2.imread(fname)
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
imhsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

# compute the absolute difference between the current frame and
# reference frame
frameDelta = cv2.absdiff( imgray, bimgray )
#frameDelta = cv2.absdiff( imhsv[:,:,0], bimhsv[:,:,0] )
fd = frameDelta.copy()

# Filter, while preserving edges
filt = cv2.bilateralFilter(fd, 11, 17, 17)

# Get thresholded image
ret,thr = cv2.threshold(filt,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Dilate the thresholded image
dkernel = np.ones((5,5),np.uint8)
dth = cv2.dilate(thr,dkernel,iterations = 3)
#ekernel = np.ones((10,10),np.uint8)
#dth = cv2.erode(dth,ekernel,iterations = 2)

# Contour the edges
# all contours
#cim, cnts, h = cv2.findContours(dth.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# only parent contours
#cim, cnts, h = cv2.findContours(dth.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cim, cnts, h = cv2.findContours(thr.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort by area
Cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
C = Cnts[0]

# Get an image where convex hull of all contours are filled in
imfill = np.zeros_like(imgray)
for c in cnts:
    hull = cv2.convexHull(c)
    cv2.drawContours( imfill, [c], -1, 255, -1 )


# Put the biggest contours in an image
Cim = np.zeros_like(imgray)
#cv2.drawContours( Cim, Cnts, -1, (255,0,0), 5 )
cv2.drawContours( Cim, [C], -1, (255,0,0), -1 )

#
peri = cv2.arcLength(C, True)
approx = cv2.approxPolyDP(C, 0.1*peri, True)

aim = imgray.copy()
cv2.drawContours( aim, [approx], -1, (255,0,0), 5 )

## Plot the delta, and filtered delta
#plt.figure()
#
#plt.subplot(1,2,1)
#plt.imshow(fd,'gray')
#
#plt.subplot(1,2,2)
#plt.imshow(filt,'gray')


# Plot the thresholded image
plt.figure()
plt.subplot(2,1,1)
plt.imshow(thr,'gray')
plt.subplot(2,1,2)
plt.imshow(dth,'gray')
plt.title('thresholded image')

## Plot all contours
#plt.figure()
#plt.imshow(cim,'gray')

# Plot big contours
plt.figure()
plt.imshow(Cim,'gray')
plt.title('Biggest Contour Filled In')

## Plot approx
#plt.figure()
#plt.imshow(aim,'gray')

# Plot all contours filled in
plt.figure()
plt.imshow(imfill,'gray')
plt.title('all contours filled in')

plt.show()


