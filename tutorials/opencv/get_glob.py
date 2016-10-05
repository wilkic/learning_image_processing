import cv2
import numpy as np
from matplotlib import pyplot as plt

def get_max_contour( contours ):
    Smax = 0
    for c in contours:
        S = cv2.contourArea(c)
        if S > Smax:
            Smax = S
            cmax = c
    return cmax

plt.close('all')

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
fd = frameDelta.copy()


# threshold it
n = 2
gray_blur = cv2.GaussianBlur(fd, (3, 3), 0)
adapt_thresh_im = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
max_thresh, thresh_im = cv2.threshold(fd, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
thresh = cv2.bitwise_or(adapt_thresh_im, thresh_im)

#thresh = cv2.threshold(fd, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]


# noise removal
n = 2
kernel = np.ones((n,n),np.uint8)
dull = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
di = cv2.dilate(dull,kernel,iterations=3)

gb = cv2.GaussianBlur(dull,(3,3),0)



b, fc, h = cv2.findContours(frameDelta.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
b, tc, h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
b, dc, h = cv2.findContours(dull,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
b, dic, h = cv2.findContours(di,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
b, gc, h = cv2.findContours(gb,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


ftc = get_max_contour(fc)
mtc = get_max_contour(tc)
mdc = get_max_contour(dc)
mdic = get_max_contour(dic)
mgc = get_max_contour(gc)


z = np.zeros_like(frameDelta)
cv2.drawContours(z, [ftc], -1, (100,0,50), 3)
cv2.drawContours(thresh, mtc, -1, (100,0,50), 3)
cv2.drawContours(dull, mdc, -1, (100,0,50), 3)
cv2.drawContours(di, mdic, -1, (100,0,50), 3)
cv2.drawContours(gb, mgc, -1, (100,0,50), 3)

plt.figure()
#plt.imshow(frameDelta)
plt.imshow(z)
plt.show()
import sys
sys.exit()

plt.ion()

plt.figure()
plt.imshow(frameDelta,'gray')
#plt.imshow(frameDelta)
plt.title('diff')

plt.figure()
import sys
sys.exit()

plt.figure()
#plt.imshow(thresh,'gray')
plt.imshow(thresh)
plt.title('thresh')

plt.figure()
#plt.imshow(dull,'gray')
plt.imshow(dull)
plt.title('dull')

plt.figure()
#plt.imshow(di,'gray')
plt.imshow(di)
plt.title('dilate')

plt.figure()
#plt.imshow(gb,'gray')
plt.imshow(di)
plt.title('gBlur')

plt.show()

plt.figure()

plt.ioff()




