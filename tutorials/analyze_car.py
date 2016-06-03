
import numpy as np
import pylab
import mahotas as mh

import matplotlib.pyplot as plt

import ipdb

plt.ion()

tc = mh.imread('/home/acp/Projects/ggp/next_car/two_cars.jpg')

tcm = tc[:,:,0];


pylab.figure(figsize=(10, 3.6))

pylab.imshow(tcm)
#pylab.gray()
pylab.colorbar()
pylab.show()

print tcm.shape
print tcm.dtype
print tcm.max()
print tcm.min()
print tcm.mean()


#T = mh.thresholding.otsu(tc)
#pylab.imshow(tc > T)
#pylab.show()



