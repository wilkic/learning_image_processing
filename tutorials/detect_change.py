#!/usr/bin/env python

import os

import numpy as np
import pylab
import mahotas as mh

import matplotlib.pyplot as plt

import ipdb

import notifications as notify

camera1 = {
    'number': 1,
    'im_dir': '/home/acp/Projects/camera_testing/hosafe/new_closet/',
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
            'times_present': 0,
            'occupied': 0,
            'persistence_threshold': 5
        }
    ]
}

#to = ['info@goodspeedparking.com',
#      '3474005261@tmomail.net',
#      '3102452197@mms.att.net']
#to = ['info@goodspeedparking.com']
to = ['info@goodspeedparking.com',
      '3474005261@tmomail.net']

cameras = {1: camera1}

from PIL import Image, ImageDraw

#for index in range(0,100):
while 1:
    
    for c, camera in cameras.iteritems():
        
        d = camera['im_dir']
        files = [os.path.join(d, f) for f in os.listdir(d)]
        files = filter(os.path.isfile, files)
        files.sort(key=lambda x: os.path.getmtime(x))
        fname = files[-1]
        ts = fname[-18:-4]

        im = mh.imread(fname)
        
        for spot in camera['spots']:
            
            # get the polygon vertices for the spot
            shp_verts = spot['vertices']
            
            # count of spectra in which car is present
            present = 0

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
                spot['times_present'] += 1
            else:
                if spot['times_present'] >= spot['persistence_threshold']:
                    leaving = 1
                spot['times_present'] = 0
            
            # Mark as occupied once spot has been taken N times
            spot['occupied'] = spot['times_present'] == spot['persistence_threshold']
            
            # Don't allow taken to go up forever
            spot['times_present'] = min( spot['times_present'],
                                       spot['persistence_threshold'] + 10 )
            
            # When spot is flagged as occupied, notify 
            if spot['occupied']:
                notify.print_mean(spot['mean'])
                print "Present %d times" % spot['times_present']
                message = """
                Spot taken !
                means = %s """ % spot['means']
                notify.send_msg_with_jpg( message, fname, to )

            # When spot is vacated, notify too
            if leaving:
                print "Car has left"

