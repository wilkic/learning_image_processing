import numpy as np
import cv2
from openalpr import Alpr

import time
import sys
sys.path.append('..')
import notifications as notify

from matplotlib import pyplot as plt

###############################################

# How long between checks (seconds)
sleepytime = 1
#sleepytime = 30

# run for half a day
n_checks = 5
#n_checks = int( 86400. / 2 / sleepytime )

log_file = 'slog.txt'
#log_file = '/mnt/data/catch/mcatch/slog.txt'

###############################################

call = "ffmpeg -rtsp_transport tcp -r 25 -y -i rtsp://108.45.109.111:9209/live0.264 -updatefirst 1 -r 2 cam09.bmp"

###############################################

# Load the baseline image
bfilename = 'cam09_bg.bmp'
bim = cv2.imread(bfilename)
bimgray = cv2.cvtColor(bim, cv2.COLOR_BGR2GRAY)

team = ['info@goodspeedparking.com']

# Init status
occupied = False
now_occupied = False

alpr = Alpr("us","/etc/openalpr/openalpr.conf","/usr/share/openalpr/runtime_data")

for timer in range(int(n_checks)):
    
    # Collect image

    # Load test image
    fname = 'cam09.bmp'
    #fname = '/home/acp/work/camera_testing/hosafe/cam9/just_lx.bmp'
    #fname = '/home/acp/work/camera_testing/hosafe/cam9/lx.bmp'
    #fname = '/home/acp/work/camera_testing/hosafe/cam9/tess.bmp'
    #fname = '/home/acp/work/camera_testing/hosafe/cam9/bg.bmp'
    im = cv2.imread(fname)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # compute the absolute difference between the current frame and
    # reference frame
    frameDelta = cv2.absdiff( imgray, bimgray )
    fd = frameDelta.copy()

    # blur it
    blur = cv2.GaussianBlur(fd,(5,5),0)

    # fancy threshold it
    ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # get contours in it
    cim, fc, h = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # get biggest contour
    contour_info = []
    for c in fc:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)

    # only check up to 3 contours (x fingers, hopefully that 3 cars...)
    maxn = min( len(contour_info), 3 )
    
    # loop over biggest contours
    now_occupied = False
    for i in range(maxn):
        max_contour = contour_info[i]
        
        cmax = max_contour[0]
        Smax = max_contour[2]
        concave = not max_contour[1]
        
        # Make a mask from contour
        mask = np.zeros(imgray.shape,np.uint8)
        cv2.drawContours(mask,[cmax],0,255,-1)

        # Get mean of contents
        mean_val_delta = cv2.mean(fd,mask = mask)
        mean_val_im    = cv2.mean(imgray,mask = mask)
        #print "diff mean = %f" % mean_val_delta[0]
        #print "    img mean = %f" % mean_val_im[0]
        #print "    S = %f" % Smax
        
        with open(log_file,'a+') as sl:
            sl.write('%f        ' % Smax )
        
        if concave and Smax > 100e3:
            now_occupied = True

    with open(log_file,'a+') as sl:
        sl.write('\n')

    if now_occupied and not occupied:
        sub = "miniCatch found something"
        msg = "Max Area = %f" % contour_info[0][2]
        ims = im.copy()
        cv2.drawContours(ims,[contour_info[0][0]],-1,(255,0,0),15)
        sfname = 'occupied.jpg'
        cv2.imwrite(sfname,ims)
        
        res = alpr.recognize_file(fname)
        lpn = ''
        try:
            lpn = str( res['results'][0]['plate'] )
            print "LPN = %s" % lpn
        except:
            print "no dice with lpr..."

        print '%s\n%s' % (sub,msg)
        msg += '\nLPN = %s' % lpn
        notify.send_msg_with_jpg( sub, msg, sfname, team )
    
    occupied = now_occupied

    time.sleep(sleepytime)
