
import cv2
import time

vcap = cv2.VideoCapture('rtsp://108.45.109.111:561/live0.264')

i = 0
while i < 10:
    ret, frame = vcap.read()
    
    t = time.strftime( '%Y%m%dT%H%M%S', time.localtime() )

    cv2.imwrite("frame_%s.jpg" % t, frame)

    

