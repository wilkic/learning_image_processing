
import cv2
import time
import math

#vcap = cv2.VideoCapture('rtsp://108.45.109.111:561/live0.264')
vcap = cv2.VideoCapture('rtsp://108.45.109.111:557/live0.264')

i = 0
while i < 10:
    ret, frame = vcap.read()
    
    t = time.time()
    tl = time.localtime(t)
    ms = (t - math.floor(t))*1000
    ts = time.strftime( '%Y%m%dT%H%M%S', tl )
    tss = ts + ('.%d' % ms)
    
    print 'Writing frame %d at %s' % (i,tss)

    cv2.imwrite("frame_%s.jpg" % ts, frame)
    
    i += 1   

vcap.release()

