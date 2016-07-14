#!/usr/bin/env python

# image processing stuff
import numpy as np
import pylab
import mahotas as mh

# probably not needed since imported pylab
import matplotlib.pyplot as plt

# debugging
import ipdb

import sys

# emailing
import send_mean as sm


im_loc = '/home/ftpsecure/imgs/00626E489E82()_test.jpg'
#im_loc = '/home/ftpsecure/imgs/test_1.jpg'

im = mh.imread(im_loc)

imr = im[:,:,0]

mval = imr.mean()

print 'Image mean is %f' % mval

sm.print_mean( mval )

print 'Emailing...'

to = ['info@goodspeedparking.com',
      '3474005261@tmomail.net',
      '3102452197@mms.att.net']

sm.send_mean( mval, to )

print 'Complete'

