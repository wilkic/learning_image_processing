
import cv2
import time
import math
from openalpr import Alpr
import pprint as pp

vcap = cv2.VideoCapture('rtsp://108.45.109.111:9509/live0.264')

ret, frame = vcap.read()
t = time.time()
tl = time.localtime(t)
ms = (t - math.floor(t))*1000
ts = time.strftime( '%Y%m%dT%H%M%S', tl )
tss = ts + ('.%d' % ms)
fname = "frame_%s.jpg" % ts

print 'Writing frame to %s at %s' % (fname,tss)

cv2.imwrite(fname, frame)

vcap.release()


alpr = Alpr("us","/etc/openalpr/openalpr.conf","/usr/share/openalpr/runtime_data")

res = alpr.recognize_file(fname)

with open('alpr.log','a') as out:
    pp.pprint( res, stream=out )


