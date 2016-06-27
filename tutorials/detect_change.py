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

camera1 = {
    'number': 1,
    'im_dir': '/home/cam1/current/',
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
while 1:
    
    for c, camera in cameras.iteritems():
        
        d = camera['im_dir']

        cnt_fail = 0
        while True:
            try:
                files = [os.path.join(d, f) for f in os.listdir(d)]
                files = filter(os.path.isfile, files)
                files.sort(key=lambda x: os.path.getmtime(x))
                src_name = files[-1]
                ft = os.path.split(src_name)
                fname = os.path.join( wd, ft[1] )
                copyfile( src_name, fname )
                cnt_fail = 0
                break
            except Exception:
                cnt_fail += 1
                if cnt_fail > 100:
                    msg = """
                    Viper is quitting !
                    I'm having file access issues."""
                    notify.send_msg(msg,to)
                    sys.exit()

        ts = fname[-18:-4]
        
        
        f_datetime =      dt.datetime( int(ts[0:4]),
                                       int(ts[4:6]),
                                       int(ts[6:8]),
                                       int(ts[8:10]),
                                       int(ts[10:12]),
                                       int(ts[12:14]) )

        delta_time_obj = f_datetime - camera['im_ts']
        delta_time = delta_time_obj.total_seconds()

        camera['im_ts'] = f_datetime
# TODO : don't do anything if snapshot hasn't been taken
# TODO : check for how stale snapshot is... notify if LONG
#        if delta_time > 0:
#            camera['im_ts'] = f_datetime

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
            
            # Mark as occupied once spot has been taken for time past threshold
            spot['occupied'] = spot['time_present'] >= spot['persistence_threshold']
            
            # When spot is flagged as occupied, notify 
            if spot['occupied']:
                notify.print_mean(spot['mean'])
                print "Present %d times" % spot['times_present']
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

    # delete the 'local' copy of image you processed
    os.remove(fname)

    # store the current state of the camera
    with open('camera.json','wt') as out:
        pp.pprint( camera, stream=out )


