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

# Copy it
cme = fgmask.copy()

# Filter preserving edges
filtraw = cv2.bilateralFilter(cme, 11, 17, 17)

# Copy it
filt = filtraw.copy()

ekernel = np.ones((5,5),np.uint8)
filt = cv2.erode(filt,ekernel,iterations = 1)
dkernel = np.ones((7,7),np.uint8)
filt = cv2.dilate(filt,dkernel,iterations = 2)

# Threshold the diff
ret,thr = cv2.threshold(filt.copy(),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# contour the diff
#cim, cnts, h = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cim, cnts, h = cv2.findContours(filt.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cim, cnts, h = cv2.findContours(thr.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

Cnts = sorted(cnts, key = cv2.contourArea, reverse = True)

Cim  = imgray.copy()
Cim  = np.zeros_like(imgray)
for i in range(1):
    cv2.drawContours( Cim, Cnts[i], -1, 255, -1 )

plt.figure()
plt.imshow(fgmask,'gray')
plt.title('fgmask')

#plt.figure()
#plt.imshow(cme,'gray')
#plt.title('cme')

plt.figure()
plt.imshow(filtraw,'gray')
plt.title('filtraw')

plt.figure()
plt.imshow(filt,'gray')
plt.title('filt')

plt.figure()
plt.imshow(thr,'gray')
plt.title('thr')

plt.figure()
plt.imshow(Cim,'gray')
plt.title('Cim')

#plt.ion()
plt.show()





