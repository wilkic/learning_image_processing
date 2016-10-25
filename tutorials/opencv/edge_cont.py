
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

#fname = 'cam09_24_26.bmp'
fname = '../minicatch/cam09_new25.bmp'
#fname = 'cam09.bmp'
#fname = '/home/acp/work/camera_testing/hosafe/cam9/just_lx.bmp'
#fname = '/home/acp/work/camera_testing/hosafe/cam9/lx.bmp'
#fname = '/home/acp/work/camera_testing/hosafe/cam9/tess.bmp'
#fname = '/home/acp/work/camera_testing/hosafe/cam9/bg.bmp'

im = cv2.imread(fname)
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# compute the absolute difference between the current frame and
# reference frame
frameDelta = cv2.absdiff( imgray, bimgray )
fd = frameDelta.copy()

# Filter, while preserving edges
filt = cv2.bilateralFilter(fd, 11, 17, 17)

# Get edges
edged = cv2.Canny(filt, 30, 200)

# Contour the edges
#cim, cnts, h = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cim, cnts, h = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort by area
Cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

# Put the biggest contours in an image
Cim = np.zeros_like(imgray)
#cv2.drawContours( Cim, Cnts, -1, (255,0,0), 5 )
cv2.drawContours( Cim, Cnts, -1, (255,0,0), -1 )

#
C = np.concatenate(cnts)
approx = cv2.approxPolyDP(C, 20, True)

aim = np.zeros_like(imgray)
cv2.drawContours( aim, [approx], -1, (255,0,0), 5 )

## Plot the delta, and filtered delta
#plt.figure()
#
#plt.subplot(1,2,1)
#plt.imshow(fd,'gray')
#
#plt.subplot(1,2,2)
#plt.imshow(filt,'gray')


# Plot the edges
plt.figure()
plt.imshow(edged,'gray')

# Plot all contours
plt.figure()
plt.imshow(cim,'gray')

# Plot big contours
plt.figure()
plt.imshow(Cim,'gray')

# Plot approx
plt.figure()
plt.imshow(aim,'gray')

plt.show()


