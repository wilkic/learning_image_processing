#!/usr/bin/env python

import os

import numpy as np
import pylab
import mahotas as mh

import matplotlib.pyplot as plt

import ipdb


import datetime as dt

import sys

import pprint as pp

from PIL import Image, ImageDraw

import traceback

sys.path.append(os.getcwd())

import notifications as notify
import get_image as gi



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
            'base_means': [100,100,100],
            'means': [0,0,0],
            'mean': 0,
            'tol': 15,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 20
        }
    ]
}

camera2 = {
    'number': 2,
    'port': 8092,
    'im_ts': dt.datetime(2016,06,26,00,00,00),
    'spots': [
        {
            'number': 2,
            'vertices': [(  0,  0),
                         (  0,425),
                         (400,425),
                         (400,  0)],
            'base_means': [110, 110, 110],
            'means': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 20
        }
    ]
}

to = ['info@goodspeedparking.com',
      '3474005261@tmomail.net',
      '3102452197@mms.att.net']
#to = ['info@goodspeedparking.com']

cameras = {1: camera1,
           2: camera2}

# When getting the latest image, move it to a directory
# for processing... then delete it when done.
wd = os.path.join( os.getcwd(), 'images_being_processed' )
if not os.path.exists(wd):
    os.makedirs(wd)


#for index in range(0,1):
while True:
    
    try:
        for c, camera in cameras.iteritems():
            
            # Write jpeg to image dir and
            # populate camera dict with time info
            result = gi.get_image( ip, camera, wd, to )
            
            if result['success']:
                delta_time = result['delta_time']
                fname = result['fname']
                
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
                        %s
                        Spot taken !
                        %s """ % ( dt.datetime.now(),
                                   pp.pformat( camera ) )
                        notify.send_msg_with_jpg( message, fname, to )

                    # When spot is vacated, notify too
                    if leaving:
                        message = """
                        %s
                        Car has left !
                        %s """ % ( dt.datetime.now(),
                                   pp.pformat( camera ) )
                        notify.send_msg_with_jpg( message, fname, to )
            
            else:
                msg = """
                %s
                Camera %d is not producing images !
                """ % (str(dt.datetime.now()),camera['number'])
                notify.send_msg(msg,to)
                print msg

                
            # store the current state of the camera
            json_fname = 'camera' + str(c) + '.json'
            with open(json_fname,'w') as out:
                pp.pprint( camera, stream=out )
            # cleanup:

            # delete the image that has been processed
            os.remove(fname)

            # store the current state of the camera
            json_fname = 'camera' + str(c) + '.json'
            with open(json_fname,'w') as out:
                pp.pprint( camera, stream=out )

    except Exception, e:
        traceback.print_exc()
        msg = """
        %s
        Viper is going offline due to user error !
        Check my error logs for details...
        %s """ % (str(dt.datetime.now()),str(e))
        notify.send_msg(msg,to)
        print str(e)
        sys.exit()

