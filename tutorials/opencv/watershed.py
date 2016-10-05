import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the baseline image
#bfilename = '/home/acp/Downloads/092216_1458.jpg'
bfilename = '/home/acp/work/camera_testing/hosafe/cam10/empty.bmp'
bim = cv2.imread(bfilename)
bimgray = cv2.cvtColor(bim, cv2.COLOR_BGR2GRAY)


# Load test image
#filename = '/home/acp/Downloads/092216_1455.jpg'
filename = '/home/acp/work/camera_testing/hosafe/cam10/spot28_occ.bmp'
im = cv2.imread(filename)
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# compute the absolute difference between the current frame and
# first frame
frameDelta = cv2.absdiff( imgray, bimgray )

thresh = cv2.threshold(frameDelta, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

# noise removal
n = 3
kernel = np.ones((n,n),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)


plt.figure()
plt.imshow(thresh,'gray')

plt.figure()
#plt.imshow(opening)
plt.imshow(sure_bg,'gray')
#plt.imshow(sure_fg,'gray')

#plt.ion()
plt.show()





