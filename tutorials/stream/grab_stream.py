
import cv2
import time

vcap = cv2.VideoCapture('rtsp://108.45.109.111:561/live0.264')

i = 0
while i < 10:
    ret, frame = vcap.read()
    
    t = time.localtime()
    ts = time.strftime( '%Y%m%dT%H%M%S.%f', t )
    tss = time.strftime( '%Y%m%dT%H%M%S', t )
    
    print 'Writing frame %d at %s' % (i,ts)

    cv2.imwrite("frame_%s.jpg" % tss, frame)
    
    i += 1   

vcap.release()

