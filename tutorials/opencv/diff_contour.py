import cv2
import numpy as np
from matplotlib import pyplot as plt


plt.close('all')

# Load the baseline image
#bfilename = '/home/acp/work/camera_testing/hosafe/cam10/empty.bmp'
#bfilename = '/home/acp/work/camera_testing/hosafe/cam10/empty_test.bmp'
bfilename = '../minicatch/cam09_bg.bmp'
bim = cv2.imread(bfilename)
bimgray = cv2.cvtColor(bim, cv2.COLOR_BGR2GRAY)


# Load test image
#filename = '/home/acp/work/camera_testing/hosafe/cam10/spot28_occ.bmp'
#filename = '/home/acp/work/camera_testing/hosafe/cam10/empty_test.bmp'
filename = '../minicatch/cam09.bmp'
im = cv2.imread(filename)
imgray = cv2.cvtColor(im.copy(), cv2.COLOR_BGR2GRAY)

# compute the absolute difference between the current frame and
# first frame
frameDelta = cv2.absdiff( imgray, bimgray )
fd = frameDelta.copy()

# blur it
blur = cv2.GaussianBlur(fd,(5,5),0)
#blur = fd.copy()

# fancy threshold it
ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# get contours in it
cim, fc, h = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# get biggest contour
Smax = 0
for c in fc:
    S = cv2.contourArea(c)
    if S > Smax:
        Smax = S
        cmax = c
        print Smax

contour_info = []
for c in fc:
    contour_info.append((
        c,
        cv2.isContourConvex(c),
        cv2.contourArea(c),
    ))
contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
max_contour = contour_info[0]
cmax = max_contour[0]

za = np.zeros_like(frameDelta)
cv2.drawContours(za, fc, -1, (255,0,0), 20)

z = np.zeros_like(frameDelta)
cv2.drawContours(z, [cmax], -1, (255,0,0), 20)

#imc = im.copy()
imc = frameDelta.copy()
cv2.drawContours(imc, [cmax], -1, (255,0,0), 20)

plt.figure()
plt.imshow(za)

plt.figure()
plt.imshow(z)

plt.figure()
plt.imshow(imc)

plt.show()


