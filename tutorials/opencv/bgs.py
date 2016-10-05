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

plt.figure()
plt.imshow(frameDelta)
plt.show()
import sys
sys.exit()

threshraw = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

#thresh = cv2.dilate(threshraw, None, iterations=2)
thresh = threshraw 
t = thresh.copy()

t = cv2.GaussianBlur(t,(5,5),0)

#(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#		cv2.CHAIN_APPROX_SIMPLE)
imthresh, cnts, h = cv2.findContours(t, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

lmax = 0
Ls = np.zeros(len(cnts))
Ss = np.zeros(len(cnts))
Ps = np.zeros(len(cnts))
CMs = np.zeros((len(cnts),2))
for i,c in enumerate(cnts):
    l = len(c)
    if l > lmax:
        imax = i
        lmax = l
        bigc = c
    Ls[i] = l
    Ss[i] = cv2.contourArea(c)
    Ps[i] = cv2.arcLength(c,True)
    M = cv2.moments(c)
    if np.abs(M['m00']) > 5e-14:
        CMs[i,0] = int(M['m10']/M['m00'])
        CMs[i,1] = int(M['m01']/M['m00'])


x, y, w, h = cv2.boundingRect(bigc)
imR = cv2.rectangle(imthresh, (x,y), (x + w, y + h), (0, 255, 0), 10)

images = [bim,im,frameDelta,threshraw,thresh,imthresh,imR]
nr = 2
nc = np.ceil(float(len(images))/nr)
for i,im in enumerate(images):
    plt.subplot(nr,nc,i+1)
    #plt.imshow(im,'gray')
    plt.imshow(im,'gray')


#p = np.zeros_like(imgray)
#cv2.drawContours( frameDelta, cnts, -1, (200,0,50), 3 )
#cv2.drawContours( p, [bigc], -1, (255,0,0), 3 )
#plt.figure()
#plt.imshow(p)

p = np.zeros_like(imgray)
p = cv2.rectangle(p, (x,y), (x + w, y + h), (255,0,0), 20)
cv2.drawContours( p, [bigc], -1, (255,0,0), 3 )
plt.figure()
plt.imshow(p)

#plt.ion()
plt.show()





