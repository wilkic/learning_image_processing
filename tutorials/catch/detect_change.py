#!/usr/bin/env python

import os

import numpy as np
import pylab
import mahotas as mh

import matplotlib.pyplot as plt

import ipdb

import time
import datetime as dt

import sys

import traceback

sys.path.append(os.getcwd())

import notifications as notify
import get_image as gi
import dataRecording as log

##########################################
##########################################
##########################################


sleepytime = 30


ip = "108.45.109.111"

#to = ['info@goodspeedparking.com',
#      '3474005261@tmomail.net',
#      '3102452197@mms.att.net']
to = ['info@goodspeedparking.com']

cameras = loadCameras( time.time() )

# When getting the latest image, move it to a directory
# for processing... then delete it when done.
wd = os.path.join( os.getcwd(), 'images_being_processed' )
if not os.path.exists(wd):
    os.makedirs(wd)

# Put spot logs in their own dir
sld, cld, csd = log.setupDirs( os.getcwd() )
dirs = {'sld':sld,'cld':cld,'csd':csd,'wd':wd}

spots = createSpots()

#for index in range(0,10):
while True:
    
    try:

        processCameras( ip, cameras, dirs )
        writeSpotsFromCameras( cameras, spots )

        processPayments( spots )

        writeTable( spots )

    except Exception, e:
        traceback.print_exc()
        msg = """
        %s
        Catch is going offline due to user error !
        Check my error logs for details...
        %s """ % (str(dt.datetime.now()),str(e))
        notify.send_msg(msg,to)
        print str(e)
        sys.exit()

    # Do it all over again, after some rest
    time.sleep(sleepytime)


