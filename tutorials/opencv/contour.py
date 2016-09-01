import cv2
import numpy as np
from matplotlib import pyplot as plt

#filename = 'van_spot17.jpg'
filename = '/home/acp/Downloads/spot37_occupied.jpg'

im = cv2.imread(filename)

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

#ret,thresh = cv2.threshold(imgray,127,255,0)
th1 = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)


#im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
thc = th1.copy()
thc, contours, hierarchy = cv2.findContours(thc,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


blur = cv2.GaussianBlur(imgray,(5,5),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
th3c = th3.copy()
th3c, contours3, hierarchy = cv2.findContours(th3c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(thc, contours, -1, (255,0,0), 3)
imc = im.copy()
cv2.drawContours(imc, contours, -1, (100,0,50), 3)

im3c = im.copy()
cv2.drawContours(im3c, contours3, -1, (200,0,50), 3)

#for h,cnt in enumerate(contours):
#    mask = np.zeros(imgray.shape,np.uint8)
#    cv2.drawContours(mask,[cnt],0,255,-1)
#    mean = cv2.mean(im,mask = mask)

#cv2.drawContours(im,contours,-1,(0,255,0), 3)

#cv2.imshow('image',im)
#cv2.waitKey(1000)
#cv2.destroyAllWindows()

#if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()

#cv2.imwrite('contours.jpg',im)

lmax = 0
Ls = np.zeros(len(contours3))
Ss = np.zeros(len(contours3))
Ps = np.zeros(len(contours3))

for i,c in enumerate(contours3):
    l = len(c)
    if l > lmax:
        imax = i
        lmax = l
        bigc = c
    Ls[i] = l
    Ss[i] = cv2.contourArea(c)
    Ps[i] = cv2.arcLength(c,True)

imC = im.copy()
cv2.drawContours(imC, [bigc], -1, (200,0,50), 3)


images = [im, th1, thc, imc, th3, im3c, imC]
nr = 2
nc = np.ceil(float(len(images))/nr)
for i,im in enumerate(images):
    plt.subplot(nr,nc,i+1)
    plt.imshow(im,'gray')
plt.show()

