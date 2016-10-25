import cv2
import numpy as np
from matplotlib import pyplot as plt

import os
import sys

import time

###############################
######## Configuration ######## 
###############################

Sthresh = 100e3
n_max_imgs_per_seq = 250
n_min_imgs_per_seq = 10
n_seqs_max = 10

frame_rate = 5
sleepytime = max( 1. / frame_rate - 0.15, 0.001 )

#n_steps = 2
n_steps = int( 300. / sleepytime )
#n_steps = int( 86400. / sleepytime )

###############################
###############################
###############################


# Load the baseline image
bfilename = 'camX_baseline.bmp'
bim = cv2.imread(bfilename)
bimgray = cv2.cvtColor(bim, cv2.COLOR_BGR2GRAY)


# get a subtractor
#fgbg = cv2.createBackgroundSubtractorMOG2()
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)


# init with empty image
fgmask = fgbg.apply(bimgray)


# Current image name
filename = 'camX.bmp'


n_seqs = 0
n_imgs = 0
i_found = 0

# Loop
tnow = time.time()
for i in range(n_steps):
    twas = tnow
    tnow = time.time()
    dt = tnow - twas

    # Sleep time between frames every iteration
    time.sleep(sleepytime)
    
    # Load current image
    b = os.path.getsize(filename)
    if b < 6220800:
        print 'b = %f' % b
        continue
    im = cv2.imread(filename)
    try:
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    except:
        print 'failed to convert to gray'
        continue

    # Apply subtraction
    try:
        fgmask = fgbg.apply(imgray)
    except:
        print 'failed to apply subtraction'
        continue
    
    # Copy it
    dif = fgmask.copy()
    
    # Filter it
    filtraw = cv2.bilateralFilter(dif, 11, 17, 17)
    
    # Copy it
    filt = filtraw.copy()

    # Erode noise
    ekernel = np.ones((5,5),np.uint8)
    filt = cv2.erode(filt,ekernel,iterations = 1)
    
    # Dilate (smear) the goods [twice]
    dkernel = np.ones((7,7),np.uint8)
    filt = cv2.erode(filt,dkernel,iterations = 2)
    
    # Threshold to keep all the goods the same
    ret,thr = cv2.threshold(filt.copy(),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Contour the thresh
    cim, cnts, h = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort by contour size
    Cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
    
    # Is biggest big enough?
    if not Cnts:
        print 'No contours'
        print 'dt = %f' % dt
        continue
    C = Cnts[0]
    S = cv2.contourArea(C)
    print 'S = %f' % S
    if S > Sthresh:
        
        # If 1st image in sequence, denote it as such
        if n_imgs == 0:
            i_found = i
        
        # Increment number of images
        n_imgs += 1
        
        # Only keep logging images if continuously logging winners
        if n_imgs > 1 and i_found < i - 1:
            
            # Mark sequence as complete if min number of contiguous
            # frames were logged
            if n_imgs > n_min_imgs_per_seq:
                n_seqs += 1
            
            # Restart the sequence
            n_imgs = 0
            continue
        

        # Stop logging sequence if max frames were recorded
        if n_imgs > n_max_imgs_per_seq:
            n_imgs = 0
            n_seqs += 1

            # Stop logging sequences if max sequences were recorded
            if n_seqs > n_seqs_max:
                sys.exit()
        
        
        # Record counter as having an image
        i_found = i

        # Sequence dir where to log image
        seq_loc = 'v%d' % n_seqs

        # Make sequence dir if not there
        if not os.path.isdir(seq_loc):
            os.mkdir(seq_loc)
        
        # Draw contour on image, save it
        Cim  = im.copy()
        cv2.drawContours( Cim, [C], -1, (255,0,255), 15 )
        
        imfname = '%s/im%d.jpg' % (seq_loc,n_imgs)
        cv2.imwrite(imfname,Cim)

        print 'delta time = %f' % dt


    
