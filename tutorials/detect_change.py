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

import pprint as pp
import csv as csv

from PIL import Image, ImageDraw

import traceback

sys.path.append(os.getcwd())

import notifications as notify
import get_image as gi


##########################################
##########################################
##########################################


sleepytime = 30

ip = "108.45.109.111"

camera1 = {
    'number': 1,
    'port': 9001,
    'im_ts': time.time(),
    'spots': [
        {
            'number': 1,
            'vertices': [(   0,   0),
                         (   0,  30),
                         ( 150,  60),
                         ( 150,   0)],
            'base_means': [118,123,127],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 15,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 2,
            'vertices': [(   0, 90),
                         (   0, 290),
                         ( 224, 230),
                         ( 224, 110)],
            'base_means': [117,117,115],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 15,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 3,
            'vertices': [(   0, 310),
                         (   0, 400),
                         ( 224, 400),
                         ( 224, 250)],
            'base_means': [119,119,117],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 15,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        }
    ]
}

camera2 = {
    'number': 2,
    'port': 9002,
    'im_ts': time.time(),
    'spots': [
        {
            'number': 4,
            'vertices': [(   0, 215),
                         (   0, 370),
                         ( 100, 400),
                         ( 224, 400),
                         ( 224, 210)],
            'base_means': [126,126,125],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 5,
            'vertices': [(   0,  50),
                         (   0, 200),
                         ( 224, 195),
                         ( 224,   0),
                         ( 170,   0)],
            'base_means': [130,130,131],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        }
    ]
}

camera3 = {
    'number': 3,
    'port': 9003,
    'im_ts': time.time(),
    'spots': [
        {
            'number': 6,
            'vertices': [(   0, 280),
                         (   0, 380),
                         (  35, 400),
                         ( 224, 400),
                         ( 224, 330)],
            'base_means': [102,102,101],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 7,
            'vertices': [(   0, 130),
                         (   0, 265),
                         ( 224, 310),
                         ( 224, 105)],
            'base_means': [122,123,121],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 8,
            'vertices': [(   0,  20),
                         (   0, 115),
                         ( 224,  85),
                         ( 224,   0),
                         (  40,   0)],
            'base_means': [137,137,140],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        }
    ]
}

camera4 = {
    'number': 4,
    'port': 9004,
    'im_ts': time.time(),
    'spots': [
        {
            'number': 9,
            'vertices': [(  30, 275),
                         (  30, 335),
                         ( 115, 400),
                         ( 224, 400),
                         ( 224, 390)],
            'base_means': [120,121,119],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 10,
            'vertices': [(  30, 165),
                         (  30, 260),
                         ( 224, 370),
                         ( 224, 240)],
            'base_means': [121,122,119],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 11,
            'vertices': [(  30,  40),
                         (  30, 150),
                         ( 224, 220),
                         ( 224,  40)],
            'base_means': [119,119,119],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        }
    ]
}

camera5 = {
    'number': 5,
    'port': 9005,
    'im_ts': time.time(),
    'spots': [
        {
            'number': 12,
            'vertices': [(   0, 310),
                         (   0, 400),
                         ( 224, 400),
                         ( 224, 360)],
            'base_means': [99,101,103],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 13,
            'vertices': [(   0, 135),
                         (   0, 290),
                         ( 224, 330),
                         ( 224,  85)],
            'base_means': [122,122,121],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        },
        {
            'number': 14,
            'vertices': [(   0,  20),
                         (   0, 115),
                         ( 224,  60),
                         ( 224,   0),
                         (  30,   0)],
            'base_means': [119,119,121],
            'means': [0,0,0],
            'sigs': [0,0,0],
            'maxs': [0,0,0],
            'mins': [0,0,0],
            'mean': 0,
            'tol': 10,
            'time_present': 0,
            'occupied': 0,
            'persistence_threshold': 145
        }
    ]
}

#to = ['info@goodspeedparking.com',
#      '3474005261@tmomail.net',
#      '3102452197@mms.att.net']
to = ['info@goodspeedparking.com']

cameras = {1: camera1,
           2: camera2,
           3: camera3,
           4: camera4,
           5: camera5}

# When getting the latest image, move it to a directory
# for processing... then delete it when done.
wd = os.path.join( os.getcwd(), 'images_being_processed' )
if not os.path.exists(wd):
    os.makedirs(wd)

# Put spot logs in their own dir
sld = os.path.join( os.getcwd(), 'spot_logs' )
if not os.path.exists(sld):
    os.makedirs(sld)

# Put camera logs in their own dir
cld = os.path.join( os.getcwd(), 'camera_logs' )
if not os.path.exists(cld):
    os.makedirs(cld)

# Put camera states in their own dir
csd = os.path.join( os.getcwd(), 'camera_states' )
if not os.path.exists(csd):
    os.makedirs(csd)

failure_notifications = 0

#for index in range(0,10):
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
                        spot['sigs'][color] = imc[shp_mask].std()
                        spot['maxs'][color] = imc[shp_mask].max()
                        spot['mins'][color] = imc[shp_mask].min()
                        
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
                        ts_gmt = time.gmtime(camera['im_ts'])
                        message = """
                        %s
                        Spot taken !
                        %s """ % ( time.asctime(ts_gmt),
                                   pp.pformat( camera ) )
                        notify.send_msg_with_jpg( message, fname, to )

                    # When spot is vacated, notify too
                    if leaving:
                        ts_gmt = time.gmtime(camera['im_ts'])
                        message = """
                        %s
                        Car has left !
                        %s """ % ( time.asctime(ts_gmt),
                                   pp.pformat( camera ) )
                        notify.send_msg_with_jpg( message, fname, to )

                    # Log spot data
                    slog_data = [camera['im_ts'], spot['time_present']] + spot['means'] + spot['sigs'] + spot['maxs'] + spot['mins']
                    slog_fname = 'spot' + str(spot['number']) + '.log'
                    slog_ffname = os.path.join(sld,slog_fname)
                    with open(slog_ffname,'a') as l:
                        w = csv.writer(l)
                        w.writerow(slog_data)
                
                # Reset failure notification log
                failure_notifications = 0

            else:
                msg = """
                %s
                Camera %d is not producing images !
                """ % (time.asctime(),camera['number'])
                if failure_notifications < 5:
                    notify.send_msg(msg,to)
                    failure_notifications += 1
                elif failure_notifications == 5:
                    msg += """
                    Camera is BROKEN
                    -- DONE SENDING MESSAGES LIKE THIS"""
                print msg

                
            # cleanup:

            # delete the image that has been processed
            os.remove(fname)

            # store the current state of the camera
            dict_fname = 'camera' + str(c) + '.dict'
            dict_ffname = os.path.join(csd,dict_fname)
            with open(dict_ffname,'w') as out:
                pp.pprint( camera, stream=out )
            
            # append the state to the log
            dict_fname = 'camera' + str(c) + '_dict.log'
            dict_ffname = os.path.join(cld,dict_fname)
            with open(dict_ffname,'a') as out:
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

    # Do it all over again, after some rest
    time.sleep(sleepytime)


