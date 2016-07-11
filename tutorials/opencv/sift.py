import cv2
import numpy as np

filename = '/home/acp/Projects/ggp/cam_images/camera1/spot2_occupied.jpg'
#filename = '/home/acp/Projects/ggp/cam_images/camera1/snap20160707185220.jpg'

img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT()
kp = sift.detect(gray,None)

img=cv2.drawKeypoints(gray,kp)

cv2.imwrite('sift_keypoints.jpg',img)

