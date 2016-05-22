
import numpy as np
import pylab
import mahotas as mh

import ipdb

tc = mh.imread('two_cars.jpg')

pylab.imshow(tc)
pylab.gray()
pylab.show()

print tc.shape
print tc.dtype
print tc.max()
print tc.min()

T = mh.thresholding.otsu(tc)
pylab.imshow(tc > T)
pylab.show()



