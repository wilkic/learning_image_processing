
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

blur = cv2.GaussianBlur(fd,(5,5),0)
th = cv2.adaptiveThreshold(fd,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,55,2)

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()

# Detect blobs.
keypoints = detector.detect(th)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(imgray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 

plt.figure()
plt.imshow(im_with_keypoints)
plt.show()


