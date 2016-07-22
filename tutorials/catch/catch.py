#!/usr/bin/env python

import os

import numpy as np
import pylab

import matplotlib.pyplot as plt

import time
import datetime as dt

import sys

import traceback

sys.path.append(os.getcwd())
import dataRecording as log
import loadCameras as lc
import processSpots
import processCameras
import processApi
import writeTable

sys.path.append("..")
import notifications as notify
import get_image as gi

##########################################
##########################################
##########################################


sleepytime = 30

nSpots = 49
monthlies = [39, 40, 41, 42]

timePresentBeforeOccupied = 60
violationThresh = 600

ip = "108.45.109.111"

#to = ['info@goodspeedparking.com',
#      '3474005261@tmomail.net',
#      '3102452197@mms.att.net']
toall = ['info@goodspeedparking.com',
      '3474005261@tmomail.net']
to = ['info@goodspeedparking.com']

threshSurf = 400
edgeLims = [100, 200]


cameras = lc.loadCameras( time.time(), threshSurf, edgeLims, timePresentBeforeOccupied )

# When getting the latest image, move it to a directory
# for processing... then delete it when done.
wd = os.path.join( os.getcwd(), 'images_being_processed' )
if not os.path.exists(wd):
    os.makedirs(wd)

cd = os.path.join( os.getcwd(), 'current_images' )
if not os.path.exists(cd):
    os.makedirs(cd)

vd = os.path.join( os.getcwd(), 'images_of_violations' )
if not os.path.exists(vd):
    os.makedirs(vd)

# Put spot logs in their own dir
sld, cld, csd = log.setupDirs( os.getcwd() )
dirs = {'sld':sld,'cld':cld,'csd':csd,'wd':wd,'cd':cd}

# Create the list of spots
spots = processSpots.create(nSpots,monthlies)

#for index in range(0,3):
while True:
    
    try:

        processCameras.processCameras( ip, cameras, dirs, to )
        
        processSpots.write( cameras, spots )
        
        processApi.processApi( spots )
        
        processSpots.judge( spots, violationThresh, toall, cd, vd )

        writeTable.writeTable( spots )

    except Exception, e:
        traceback.print_exc()
        msg = """
        %s
        Catch is going offline due to user error !
        Check my error logs for details...
        %s """ % (str(dt.datetime.now()),str(e))
        notify.send_msg(msg,toall)
        print "%s\n\n%s" % (msg, str(e))
        sys.exit()

    # Do it all over again, after some rest
    time.sleep(sleepytime)


