
import os

import numpy as np
import pylab
import mahotas as mh
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import json

import ipdb



plt.close("all")



camera = {
    'number': 2,
    'im_full_path': '/home/acp/Projects/camera_testing/hosafe/garage_testing_062216/cam1_20160622121838.jpg',
    'spots': [
        {
            'number': 30,
            'vertices': [( 350,   0),
                         ( 350, 380),
                         ( 720, 250),
                         ( 720,   0)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 31,
            'vertices': [( 350, 420),
                         ( 350, 850),
                         ( 720,1000),
                         ( 720, 300)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 32,
            'vertices': [( 350, 900),
                         ( 350,1200),
                         ( 420,1280),
                         ( 720,1280),
                         ( 720,1050)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 47,
            'vertices': [(  25, 820),
                         (  25,1010),
                         ( 100,1100),
                         ( 100, 920)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 48,
            'vertices': [(  20, 690),
                         (  25, 810),
                         ( 100, 910),
                         ( 100, 710)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 49,
            'vertices': [(  20, 510),
                         (  20, 680),
                         ( 100, 700),
                         ( 100, 460)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        }
    ]
}


fname = camera['im_full_path']

im = mh.imread(fname)

#pylab.ion()
#pylab.figure(figsize=(10,6))
#pylab.imshow(im)
#pylab.colorbar()
#pylab.show()
#break

for color in range(0,3):
#for color in range(0,1):
    
    imc = im[:,:,color]
    imm = np.zeros(imc.shape)

    for spot in camera['spots']:
        
        shp_verts = spot['vertices']

        shp = Image.new( 'L', imc.shape, 0 )
        
        ImageDraw.Draw(shp).polygon( shp_verts, outline=1, fill=1 )
        
        shp_mask = np.array(shp).transpose().astype(bool)
        
        imct = np.copy(imc)
        imct[np.invert(shp_mask)] = 0
        
        #pylab.figure(figsize=(10,6))
        #pylab.imshow(imct)
        #pylab.colorbar()
        #pylab.show()
        
        imm[shp_mask] = imc[shp_mask]

        spot['means'][color] = imc[shp_mask].mean()

    pylab.ion()
    pylab.figure(figsize=(10,6))
    pylab.imshow(imc)
    pylab.colorbar()
    pylab.show()

    pylab.ion()
    pylab.figure(figsize=(10,6))
    pylab.imshow(imm)
    pylab.colorbar()
    pylab.show()


