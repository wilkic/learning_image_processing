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

data_dir = os.getcwd()
#data_dir = '/mnt/data/catch/'

nSpots = 49
monthlies = [38, 39, 40, 41, 42]

timePresentBeforeOccupied = 60
violationThresh = 900

ip = "108.45.109.111"

spam = True 

#to = ['info@goodspeedparking.com',
#      '3474005261@tmomail.net',
#      '3102452197@mms.att.net']
toall = ['info@goodspeedparking.com',
      '3474005261@tmomail.net']
to = ['info@goodspeedparking.com']

threshSurf = 400
edgeLims = [100, 200]


os.environ['TZ'] = 'US/Eastern'
time.tzset()

cameras = lc.loadCameras( time.time(), threshSurf, edgeLims, timePresentBeforeOccupied )

# When getting the latest image, move it to a directory
# for processing... then delete it when done.
wd = os.path.join( data_dir, 'images_being_processed' )
if not os.path.exists(wd):
    os.makedirs(wd)

cd = os.path.join( data_dir, 'current_images' )
if not os.path.exists(cd):
    os.makedirs(cd)

vd = os.path.join( data_dir, 'images_of_violations' )
if not os.path.exists(vd):
    os.makedirs(vd)

ud = os.path.join( data_dir, 'images_of_undetections' )
if not os.path.exists(ud):
    os.makedirs(ud)

# Put spot logs in their own dir
sld, cld, csd = log.setupDirs( data_dir )
dirs = {'sld':sld,'cld':cld,'csd':csd,'wd':wd,'cd':cd}

# Create the list of spots
spots = processSpots.create(nSpots,monthlies,cameras,ip)

#for index in range(0,3):
while True:
    
    try:

        processCameras.processCameras( cameras, dirs, to, spam )
        
        processSpots.write( cameras, spots )
        
        processApi.processApi( data_dir, spots, monthlies, toall )
        
        processSpots.judge( spots, violationThresh, monthlies, toall, cd, vd, ud )

        writeTable.writeTable( spots )

    except Exception, e:
        tb = traceback.format_exc()
        msg = """
        %s
        Catch is going offline due to user error !
        Check my error logs for details...
        
        Exception:
        %s
        
        Traceback:
        %s""" % (str(dt.datetime.now()),str(e),tb)
        notify.send_msg('Error',msg,toall)
        print "%s\n\n%s" % (msg, str(e))
        sys.exit()

    # Do it all over again, after some rest
    time.sleep(sleepytime)


