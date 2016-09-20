#!/usr/bin/env python

import os

import numpy as np
import pylab

import time

import sys
sys.path.append("../catch/.")
import analyzeImage as ai
import determinePresence as dp

sys.path.append("..")
import notifications as notify

import traceback


##########################################
##########################################
##########################################


sleepytime = 3

data_dir = os.getcwd()
#data_dir = '/mnt/data/catch/'


threshSurf = 400
edgeLims = [100, 200]


os.environ['TZ'] = 'US/Eastern'
time.tzset()


t0 = time.time();

camera = {
    'im_ts': t0,
    'threshSurf': 400,
    'edgeLims': [100, 200],       
    'spots': [
        {
            'number': 100,
            'vertices': np.array(
                        [[ 410,   0],
                         [ 690,   0],
                         [ 640, 330],
                         [1280, 350],
                         [1280, 720],
                         [   0, 720]]),
            'base_means': [127,128,128],
            'base_nEdges': 8000,
            'base_nKeys': 110,
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'meanThresh': 50,
            'edgeThresh': 500,
            'keyThresh': 50,
            'detectionType': 'ke',
            'timePresent': 0,
            'timeOccupied': 0,
            'occupationStartTime': t0,
            'occupationEndTime': t0,
            'occupationThresh': 1
        },
    ]
}

n_logs = 0

log = open('log','w')

#for index in range(0,3):
while True:
    
    try:
        

        # Get picture
        call = "ffmpeg -rtsp_transport tcp -y -i "
        in_url = "rtsp://108.45.109.111:9204/live0.264"
        out_args = " -vframes 1 "
        im_name = "tmp.bmp"
        call += in_url + out_args + im_name
        
        os.system(call)


        # Is something going on ?
        ai.analyzeImage( im_name, camera )

        spot = camera['spots'][0]
        present = dp.determinePresence( spot )
        
        log.write("nkeys = %d" % spot['nKeys'])
        log.write('      ')
        log.write("nedges = %d\n" % spot['nEdges'])
        log.write('\n\n')
        
        if present:
            
            n_logs += 1
            
            log.write("\tI see something: %d\n" % n_logs)
            log.write("\tnkeys = %d\n" % spot['nKeys'])
            log.write("\tnedges = %d\n" % spot['nEdges'])
            log.write('\n\n')

            ncall = "ffmpeg -rtsp_transport tcp -y -i "
            in_url = "rtsp://108.45.109.111:9204/live0.264"
            out_args = " -vframes 120 -r 24 "
            dir_name = "log%d" % n_logs
            im_name = "tmp%03d.bmp"
            fim_name = dir_name + '/' + im_name
            ncall += in_url + out_args + fim_name
            
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            os.system(ncall)

            if n_logs == 9:
                sys.exit()

    except Exception, e:
        tb = traceback.format_exc()
        msg = """
        %s
        Catch2 is going offline due to user error !
        Check my error logs for details...
        
        Exception:
        %s
        
        Traceback:
        %s""" % (time.asctime(),str(e),tb)
        print "%s\n\n%s" % (msg, str(e))
        notify.send_msg('Error',msg,toall)
        sys.exit()

    # Do it all over again, after some rest
    time.sleep(sleepytime)


