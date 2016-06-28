#!/usr/bin/env python

import os

import numpy as np
import pylab
import mahotas as mh

import matplotlib.pyplot as plt

import ipdb

import notifications as notify

import datetime as dt

import sys

import pprint as pp

from shutil import copyfile

from PIL import Image, ImageDraw

import traceback

ip = "108.45.109.111"

camera1 = {
    'number': 1,
    'port': 8091,
    'im_ts': dt.datetime(2016,06,26,00,00,00),
    'spots': [
        {
            'number': 1,
            'vertices': [(  0,  0),
                         (  0,425),
                         (400,425),
                         (400,  0)],
#            'base_means': [119,120,118],
#            'base_means': [94,95,94],
            'base_means': [94.422767857142858, 94.507968750000003, 93.452845982142861],
            'means': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 5
        }
    ]
}

to = ['info@goodspeedparking.com',
      '3474005261@tmomail.net',
      '3102452197@mms.att.net']
#to = ['info@goodspeedparking.com']

cameras = {1: camera1}

# When getting the latest image, move it to a directory
# for processing... then delete it when done.
wd = os.path.join( os.getcwd(), 'images_being_processed' )
if not os.path.exists(wd):
    os.makedirs(wd)

#for index in range(0,100):
while True:
    
    try:
        for c, camera in cameras.iteritems():
            
            # filename of image
            fname = wd + '/snap.jpg'

            # store snapshot to processing dir (wd)
            # using wget cuz otherwise I can't open the file (urllib etc)
            url = 'http://' + ip + ':' + str(camera['port'])
            url += '/cgi-bin/getsnapshot.cgi'
            call = 'wget ' + url + ' -O ' + fname + ' >/dev/null 2>&1'
            # Verbose
            #call = 'wget ' + url + ' -O ' + fname
            
            tries = 0
            while True:
                if tries>10:
                    msg = """
                    %s
                    Camera %d is not producing images !
                    """ % (str(dt.datetime.now()),c)
                    #notify.send_msg(msg,to)
                    print msg   
                    sys.exit()

                tries += 1
                os.system(call)
                if os.stat(fname).st_size < 16000:
                    copyfile(fname, wd+'/failed_snap_'+str(tries)+'.jpg')
                    continue
                else:
                    break

            
            # get timestamp
            ts = dt.datetime.now()
            
            # get time since last image
            delta_time_obj = ts - camera['im_ts']
            delta_time = delta_time_obj.total_seconds()
            
            # set timestamp for current image
            camera['im_ts'] = ts
            
            # read image
            im = mh.imread(fname)
            
            for spot in camera['spots']:
                
                # get the polygon vertices for the spot
                shp_verts = spot['vertices']
                
                # count of spectra in which car is present
                present = 0
                
                # set the mean to zero (it gets incremented)
                spot['mean'] = 0

                for color in range(0,3):
                
                    imc = im[:,:,color]
                    
                    shp = Image.new( 'L', imc.shape, 0 )
                    
                    ImageDraw.Draw(shp).polygon( shp_verts, outline=1, fill=1 )
                    
                    shp_mask = np.array(shp).transpose().astype(bool)
                    
                    imct = np.copy(imc)
                    imct[np.invert(shp_mask)] = 0
                    
                    spot['means'][color] = imc[shp_mask].mean()
                    
                    mdiff = spot['means'][color] - spot['base_means'][color]

                    if abs( mdiff ) > spot['tol']:
                        present += 1
                    
                    spot['mean'] += spot['means'][color]

                spot['mean'] /= 3
                
                # If car is present, mark as taken
                # otherwise reset counter
                leaving = 0
                if present > 1:
                    spot['time_present'] += delta_time
                else:
                    if spot['time_present'] >= spot['persistence_threshold']:
                        leaving = 1
                    spot['time_present'] = 0
                
                # if wasn't occupied, occupance will be new
                newly_occupied = not spot['occupied']
                
                # Mark as occupied once spot has been taken for time past threshold
                spot['occupied'] = spot['time_present'] >= spot['persistence_threshold']
                
                # When spot is flagged as occupied, notify 
                if spot['occupied'] and newly_occupied:
                    notify.print_mean(spot['mean'])
                    print "Present %f seconds" % spot['time_present']
                    message = """
                    Spot taken !
                    %s """ % pp.pprint( camera )
                    notify.send_msg_with_jpg( message, fname, to )

                # When spot is vacated, notify too
                if leaving:
                    message = """
                    Car has left !
                    means = %s """ % spot['means']
                    notify.send_msg_with_jpg( message, fname, to )
        
        # cleanup:

        # delete the image that has been processed
        os.remove(fname)

        # store the current state of the camera
        with open('camera.json','wt') as out:
            pp.pprint( camera, stream=out )

    except Exception, e:
            traceback.print_exc()
            msg = """
            Viper is going offline due to user error !
            Check my error logs for details...
            %s """ % str(e)
            notify.send_msg(msg,to)
            print str(e)
            sys.exit()

