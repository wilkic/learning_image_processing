
import numpy as np
import pylab
import mahotas as mh

import matplotlib.pyplot as plt

import ipdb

plt.close("all")

camera1 = {
    'number': 1,
    'floc': '/home/acp/Projects/ggp/imgs/two_cars.png',
    'spots': [
        {
            'number': 1,
            'vertices': [(0,200),(0,800),(500,200)],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 2,
            'vertices': [(0,200),(0,800),(500,800),(400,300)],
            'mean': 0,
            'taken': 0
        }
    ]
}

camera2 = {
    'number': 2,
    'floc': '/home/acp/Projects/ggp/lot_pics/fromPhone/IMG_20160610_120207.jpg',
    'spots': [
        {
            'number': 12,
            'vertices': [(0,200),(0,800),(500,200)],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 13,
            'vertices': [(0,200),(0,800),(500,800),(400,300)],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 14,
            'vertices': [(0,200),(0,800),(500,800),(400,300)],
            'mean': 0,
            'taken': 0
        }
    ]
}

cameras = {1: camera1, 2: camera2}

im = mh.imread(cameras[1]['floc'])

imr = im[:,:,0]

shp_verts = cameras[1]['spots'][1]['vertices']

from PIL import Image, ImageDraw
shp = Image.new( 'L', imr.shape, 0 )
ImageDraw.Draw(shp).polygon( shp_verts, outline=1, fill=1 )
shp_mask = np.array(shp).transpose().astype(bool)
imrt = np.copy(imr)
imrt[np.invert(shp_mask)] = 0



pylab.ion()
pylab.figure(figsize=(10,6))
pylab.imshow(imr)
pylab.colorbar()
pylab.show()

pylab.figure(figsize=(10,6))
pylab.imshow(imrt)
pylab.colorbar()
pylab.show()


