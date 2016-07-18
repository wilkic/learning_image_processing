
import numpy as np
import pylab
import matplotlib.pyplot as plt
import cv2

import ipdb

plt.close("all")

camera1 = {
    'number': 1,
    'floc': '/home/acp/work/ggp/imgs/two_cars.png',
    'spots': [
        {
            'number': 1,
            'vertices': np.array([[200,200],[0,800],[500,200]]),
            'mean': 0,
            'taken': 0
        },
        {
            'number': 2,
            'vertices': np.array([[0,200],[0,800],[500,800],[400,300]]),
            'mean': 0,
            'taken': 0
        }
    ]
}

camera2 = {
    'number': 2,
    'floc': '/home/acp/work/ggp/lot_pics/fromPhone/IMG_20160610_120207.jpg',
    'spots': [
        {
            'number': 12,
            'vertices': np.array([[0,200],[0,800],[500,200]]),
            'mean': 0,
            'taken': 0
        },
        {
            'number': 13,
            'vertices': np.array([[0,200],[0,800],[500,800],[400,300]]),
            'mean': 0,
            'taken': 0
        },
        {
            'number': 14,
            'vertices': np.array([[0,200],[0,800],[500,800],[400,300]]),
            'mean': 0,
            'taken': 0
        }
    ]
}

cameras = {1: camera1, 2: camera2}

im = cv2.imread(cameras[1]['floc'])

imr = im[:,:,0]

verts = cameras[1]['spots'][1]['vertices']
#mask = np.zeros((imr.shape[0],imr.shape[1]))
mask = np.zeros_like(imr)
cv2.fillConvexPoly(mask,verts,1)
#cv2.fillPoly(mask,np.array(verts),1)
mask = mask.astype(bool)

imm = np.zeros_like(imr)
imm[mask] = imr[mask]

#import pylab
#pylab.ion()
#pylab.figure()
#pylab.imshow(imr)
#pylab.show()
#
#pylab.ion()
#pylab.figure()
#pylab.imshow(imm)
#pylab.show()



cv2.imshow('orig',imr)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(0)
cv2.waitKey(0)
cv2.waitKey(0)
cv2.destroyAllWindows()


cv2.imshow('orig',imm)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(0)
cv2.waitKey(0)
cv2.waitKey(0)
cv2.destroyAllWindows()


