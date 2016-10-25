import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = '/home/acp/work/camera_testing/hosafe/camX/now.bmp'

# get a subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

keep_going = True
while keep_going:

    # Load image
    im = cv2.imread(filename)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # subtract
    fgmask = fgbg.apply(imgray)

    plt.figure(1)
    plt.imshow(fgmask)

    #plt.ion()
    plt.show()





