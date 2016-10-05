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

# get a subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# init with empty image
fgmask = fgbg.apply(bimgray)

# run with full image
fgmask = fgbg.apply(imgray)


plt.figure()
plt.imshow(fgmask)

#plt.ion()
plt.show()





