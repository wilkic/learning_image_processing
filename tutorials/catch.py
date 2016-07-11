
import os

import numpy as np
import pylab
import mahotas as mh
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import json
import pprint as pp

import ipdb

import cv2


plt.close("all")

test_camera1 = {
    'number': 1,
#    'im_full_path': '/home/acp/Projects/ggp/cam_images/camera1/snap20160705224323.jpg',
    'im_full_path': '/home/acp/Projects/ggp/cam_images/camera1/spot2_occupied.jpg',
    'spots': [
        {
            'number': 1,
            'vertices': [(   0,   0),
                         (   0,  30),
                         ( 150,  60),
                         ( 150,   0)],
            'base_means': [118,123,127],
            'sigs': [0,0,0]
        },
        {
            'number': 2,
            'vertices': [(   0, 90),
                         (   0, 290),
                         ( 224, 230),
                         ( 224, 110)],
            'base_means': [117,117,115],
            'sigs': [0,0,0]
        },
        {
            'number': 3,
            'vertices': [(   0, 310),
                         (   0, 400),
                         ( 224, 400),
                         ( 224, 250)],
            'base_means': [119,119,117],
            'sigs': [0,0,0]
        }
    ]
}



camera1 = {
    'number': 1,
    'im_full_path': '/home/acp/Projects/ggp/cam_images/camera1/snap20160705224323.jpg',
    'spots': [
        {
            'number': 1,
            'vertices': [(   0,   0),
                         (   0,  30),
                         ( 150,  60),
                         ( 150,   0)],
            'base_means': [118,123,127],
        },
        {
            'number': 2,
            'vertices': [(   0, 90),
                         (   0, 290),
                         ( 224, 230),
                         ( 224, 110)],
            'base_means': [117,117,115],
        },
        {
            'number': 3,
            'vertices': [(   0, 310),
                         (   0, 400),
                         ( 224, 400),
                         ( 224, 250)],
            'base_means': [119,119,117],
        }
    ]
}

camera2 = {
    'number': 2,
    'im_full_path': '/home/acp/Projects/ggp/cam_images/camera2/snap20160706230618.jpg',
    'spots': [
        {
            'number': 4,
            'vertices': [(   0, 215),
                         (   0, 370),
                         ( 100, 400),
                         ( 224, 400),
                         ( 224, 210)],
            'base_means': [126,126,125],
        },
        {
            'number': 5,
            'vertices': [(   0,  50),
                         (   0, 200),
                         ( 224, 195),
                         ( 224,   0),
                         ( 170,   0)],
            'base_means': [130,130,131],
        }
    ]
}

camera3 = {
    'number': 3,
    'im_full_path': '/home/acp/Projects/ggp/cam_images/camera3/snap20160705224324.jpg',
    'spots': [
        {
            'number': 6,
            'vertices': [(   0, 280),
                         (   0, 380),
                         (  35, 400),
                         ( 224, 400),
                         ( 224, 330)],
            'base_means': [102,102,101],
        },
        {
            'number': 7,
            'vertices': [(   0, 130),
                         (   0, 265),
                         ( 224, 310),
                         ( 224, 105)],
            'base_means': [122,123,121],
        },
        {
            'number': 8,
            'vertices': [(   0,  20),
                         (   0, 115),
                         ( 224,  85),
                         ( 224,   0),
                         (  40,   0)],
            'base_means': [137,137,140],
        },
    ]
}

camera4 = {
    'number': 4,
    'im_full_path': '/home/acp/Projects/ggp/cam_images/camera4/snap20160706230618.jpg',
    'spots': [
        {
            'number': 9,
            'vertices': [(  30, 275),
                         (  30, 335),
                         ( 115, 400),
                         ( 224, 400),
                         ( 224, 390)],
            'base_means': [120,121,119],
        },
        {
            'number': 10,
            'vertices': [(  30, 165),
                         (  30, 260),
                         ( 224, 370),
                         ( 224, 240)],
            'base_means': [121,122,119],
        },
        {
            'number': 11,
            'vertices': [(  30,  40),
                         (  30, 150),
                         ( 224, 220),
                         ( 224,  40)],
            'base_means': [119,119,119],
        },
    ]
}

camera5 = {
    'number': 5,
    'im_full_path': '/home/acp/Projects/ggp/cam_images/camera5/snap20160705224325.jpg',
    'spots': [
        {
            'number': 12,
            'vertices': [(   0, 310),
                         (   0, 400),
                         ( 224, 400),
                         ( 224, 360)],
            'base_means': [99,101,103],
        },
        {
            'number': 13,
            'vertices': [(   0, 135),
                         (   0, 290),
                         ( 224, 330),
                         ( 224,  85)],
            'base_means': [122,122,121],
        },
        {
            'number': 14,
            'vertices': [(   0,  20),
                         (   0, 115),
                         ( 224,  60),
                         ( 224,   0),
                         (  30,   0)],
            'base_means': [119,119,121],
        },
    ]
}


camera = test_camera1 


fname = camera['im_full_path']

im = mh.imread(fname)

# get edges
edges = cv2.Canny( im, 100, 200 )

ime = np.copy(im)
ime[edges==255,0] = 255
pylab.ion()
pylab.figure(figsize=(10,6))
pylab.imshow(ime)
pylab.show()
import sys; sys.exit()

# Set up keypoint threshold
#surf = cv2.SURF(400)
surf = cv2.SURF(300)

for spot in camera['spots']:
    
    shp_verts = spot['vertices']

    shp = Image.new( 'L', im[:,:,0].shape, 0 )
    
    ImageDraw.Draw(shp).polygon( shp_verts, outline=1, fill=1 )
    
    shp_mask = np.array(shp).transpose().astype('uint8')
    
    imt = np.copy(im)
    
    # get keypoints
    kp, des = surf.detectAndCompute(imt,shp_mask)
    
    # This is for viewing only -- mask is passed to keypoint detection
    imt[np.invert(shp_mask.astype(bool))] = 0
    
    # draw keypoints
    img2 = cv2.drawKeypoints(imt,kp,None,(255,0,0),4)


    pylab.ion()
    pylab.figure(figsize=(10,6))
    pylab.imshow(img2)
    #pylab.imshow(imct)
    #pylab.colorbar()
    pylab.show()

#
#    pylab.ion()
#    pylab.figure(figsize=(10,6))
#    pylab.imshow(imm)
#    pylab.colorbar()
#    pylab.show()
#
#
#for spot in camera['spots']:
#    pp.pprint(spot)
