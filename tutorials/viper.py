
import os

import numpy as np
import pylab
import mahotas as mh
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import json
import pprint as pp

import ipdb



plt.close("all")



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
            'vertices': [(   0,  50),
                         (   0, 200),
                         ( 224, 195),
                         ( 224,   0),
                         ( 170,   0)],
            'base_means': [130,130,131],
        },
        {
            'number': 5,
            'vertices': [(   0, 215),
                         (   0, 370),
                         ( 100, 400),
                         ( 224, 400),
                         ( 224, 210)],
            'base_means': [126,126,125],
        }
    ]
}

camera = camera2

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

        spot['base_means'][color] = imc[shp_mask].mean()
        

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


for spot in camera['spots']:
    pp.pprint(spot)
