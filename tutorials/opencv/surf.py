import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = '/home/acp/work/ggp/cam_images/camera1/spot2_occupied.jpg'
#filename = '/home/acp/work/ggp/cam_images/camera1/snap20160707185220.jpg'

img = cv2.imread(filename)

surf = cv2.xfeatures2d.SURF_create(400)

kp, des = surf.detectAndCompute(img,None)

img2 = cv2.drawKeypoints(img,kp,None,(255,0,0),4)

plt.imshow(img2),plt.show()

cv2.imwrite('surf_keypoints.jpg',img2)

