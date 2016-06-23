
import numpy as np
import pylab
import mahotas as mh

import matplotlib.pyplot as plt

import ipdb

plt.close("all")

camera = {
    'number': 1,
    'floc': '/home/acp/Projects/ggp/imgs/two_cars.png',
    'spots': [
        {
            'number': 1,
            'xrng': [0, 20],
            'yrng': [800, 1200],
            'mean': 0,
            'taken': 0
        },
        {
            'number': 2,
            'xrng': [30, 50],
            'yrng': [800, 1200],
            'mean': 0,
            'taken': 0
        }
    ]
}

im = mh.imread(camera['floc'])

imr = im[:,:,0]

grnd_inds = (slice(350,425), slice(200,600))
car1_inds = (slice(100,200), slice(300,650))
carpic = imr[0:400,200:800]
imrg = im[grnd_inds[0],grnd_inds[1],0]
imrc = im[car1_inds[0],car1_inds[1],0]

shp_verts = [(100,300),(100,800),(400,500)]
from PIL import Image, ImageDraw
shp = Image.new( 'L', imr.shape, 0 )
ImageDraw.Draw(shp).polygon( shp_verts, outline=1, fill=1 )
shp_mask = np.array(shp).transpose().astype(bool)
imrt = np.copy(imr)
imrt[shp_mask] = 255



pylab.ion()
pylab.figure(figsize=(10,6))
pylab.imshow(imr)
pylab.colorbar()
pylab.show()

pylab.figure(figsize=(10,6))
pylab.imshow(carpic)
pylab.colorbar()
pylab.show()

pylab.figure(figsize=(10,6))
pylab.imshow(imrg)
pylab.colorbar()
pylab.show()

pylab.figure(figsize=(10,6))
pylab.imshow(imrc)
pylab.colorbar()
pylab.show()

pylab.figure(figsize=(10,6))
pylab.imshow(imrt)
pylab.colorbar()
pylab.show()


#pylab.figure(figsize=(10,3.5))
#for i in range(0,3):
#    pn = 311 + i
#    pylab.subplot(pn)
#    pylab.imshow(im[
#    pylab.show()


