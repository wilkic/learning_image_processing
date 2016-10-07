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
#sleepytime = 11

# run for half a day
n_checks = 2
#n_checks = int( 86400. / 2 / sleepytime )

log_file = 'slog.txt'
#log_file = '/mnt/data/catch/mcatch/slog.txt'

# Contour area above which, a car is registered
Slim = 80e3

###############################################

call = "ffmpeg -rtsp_transport tcp -r 25 -y -i rtsp://108.45.109.111:9209/live0.264 -updatefirst 1 -r 2 cam09.bmp"

###############################################

# Load the baseline image
bfilename = 'cam09_bg.bmp'
bim = cv2.imread(bfilename)
bimgray = cv2.cvtColor(bim, cv2.COLOR_BGR2GRAY)

team = ['info@goodspeedparking.com']

# Init status
occupied = [False, False, False]

alpr = Alpr("us","/etc/openalpr/openalpr.conf","/usr/share/openalpr/runtime_data")

bad_count = 0
for timer in range(int(n_checks)):
    
    # By default, no one is there 
    now_occupied = [False, False, False]

    # Load test image
    if timer is 0:
        fname = 'cam09.bmp'
    else:
        fname = 'cam09_now.bmp'
    #fname = 'cam09.bmp'
    #fname = '/home/acp/work/camera_testing/hosafe/cam9/just_lx.bmp'
    #fname = '/home/acp/work/camera_testing/hosafe/cam9/lx.bmp'
    #fname = '/home/acp/work/camera_testing/hosafe/cam9/tess.bmp'
    #fname = '/home/acp/work/camera_testing/hosafe/cam9/bg.bmp'
    try:
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

        # Copy image
        ims = im.copy()
        
        # Loop over cars
        ci = 0
        while contour_info[ci][2] > Slim and ci < 3:
            
            # Grab current contour
            c = contour_info[ci][0]
            
            # Draw car contours on one image
            cv2.drawContours(ims,[c],-1,(0,0,255),15)
            
            # Empty mask
            mask = np.zeros(imgray.shape,np.uint8)

            # Get corner/dims of rectangle around contour
            x,y,w,h = cv2.boundingRect(c)

            # Make mask true within that rectangle
            mask[y:y+h,x:x+w] = 255

            # New image is like orig, but just the rectangle
            imc = cv2.bitwise_and( im, im, mask=mask )

            # Draw the contour on it
            cv2.drawContours(imc,[c],0,(255,0,200),5)
            
            # Get center of contour
            M = cv2.moments( c )
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            # Determine spot
            spotN = 24
            if cx > 475:
                spotN = 25
                if cx > 900:
                    spotN = 26
            
            # Determine current occupation
            if spotN is 24:
                now_occupied[0] = True
            elif spotN is 25:
                now_occupied[1] = True
            elif spotN is 26:
                now_occupied[2] = True

            # Write it to file
            tfname = 'spot' + str(spotN) + '.jpg'
            cv2.imwrite(tfname,imc[y:y+h,x:x+w])
            
            # Log the area
            with open(log_file,'a+') as sl:
                sl.write('%f        ' % contour_info[ci][2] )
            
            # Increment contour counter counter
            ci += 1
        
        # If not 3 spots taken, log smaller contours
        while ci < 3:
            # Log the area
            with open(log_file,'a+') as sl:
                sl.write('%f        ' % contour_info[ci][2] )
            ci += 1

        # Go to next line in log
        with open(log_file,'a+') as sl:
            sl.write('\n')
        

        # If spot occupation has changed and someone's there...
        if occupied is not now_occupied and np.any(now_occupied):
            # Write image with all biggest contours
            sfname = 'occupied.jpg'
            cv2.imwrite(sfname,ims)
            
            res = alpr.recognize_file(fname)
            lpn = ''
            try:
                lpn = str( res['results'][0]['plate'] )
                print "LPN = %s" % lpn
            except:
                print "no dice with lpr..."
            
            sub = 'Occupation has changed'
            msg = 'Spot Status = %s' % str(now_occupied)
            print '%s\n%s' % (sub,msg)
            msg += '\nLPN = %s' % lpn
            #notify.send_msg_with_jpg( sub, msg, sfname, team )
        
        # Set occupation to current status
        occupied = now_occupied

    except Exception, e:
        print e
        bad_count += 1
        if bad_count == 5:
            print "too many failures\n\t%s" % str(e)
            notify.send_msg('Error',str(e),team)
            sys.exit()


    time.sleep(sleepytime)
