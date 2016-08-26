import cv2
import numpy as np
from matplotlib import pyplot as plt

#filename = '/home/acp/work/ggp/cam_images/camera1/spot2_occupied.jpg'
filename = '/home/acp/work/ggp/cam_images/camera1/snap20160707185220.jpg'

img = cv2.imread(filename)

gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

detector = cv2.AKAZE_create()
(kps, descs) = detector.detectAndCompute(gray1, None)

img2 = cv2.drawKeypoints(img,kps,None,(0,0,255),4)

plt.imshow(img2),plt.show()

cv2.imwrite('kaze_keypoints.jpg',img2)

