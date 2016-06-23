
import os

import numpy as np
import pylab
import mahotas as mh

import matplotlib.pyplot as plt

import ipdb

plt.close("all")

camera1 = {
    'number': 1,
    'im_dir': '/home/acp/Projects/camera_testing/hosafe/garage_testing_062216/',
    'spots': [
        {
            'number': 1,
            'vertices': [(125,325),
                         (100,400),
                         (100,500),
                         (150,650),
                         (200,650),
                         (200,325)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 2,
            'vertices': [(200,700),(100,900),(100,1296),(400,1296),(400,750)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 3,
            'vertices': [(500,850),(380,1296),(600,1296)],
            'means': [0,0,0],
            'mean': 0,
            'taken': 0
        }
    ]
}

camera2 = {
    'number': 2,
    'im_dir': '/home/acp/Projects/camera_testing/hosafe/garage_testing_062216/',
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

cameras = {1: camera1, 2: camera2}

from PIL import Image, ImageDraw

for c, camera in cameras.iteritems():
    
    if c == 1:
        continue
    
    d = camera['im_dir']
    files = [os.path.join(d, f) for f in os.listdir(d)]
    files = filter(os.path.isfile, files)
    files.sort(key=lambda x: os.path.getmtime(x))
    fname = files[-1]
    ts = fname[-18:-4]

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


