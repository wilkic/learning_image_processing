
import os
import sys

#frame_rate = 2
frame_rate = 5

call = "ffmpeg -rtsp_transport tcp -r 25 -y -i rtsp://admin:@108.45.109.111:9220/live0.264 -updatefirst 1 -r %d camX.bmp" % frame_rate


import signal
def signal_term_handler(signal, frame):
    print 'got SIGTERM'
    sys.exit(0)
 
signal.signal(signal.SIGINT, signal_term_handler)

while True:
    try:
        os.system(call)
    except (KeyboardInterrupt, SystemExit):
        for i in range(100):
            print "YOU ARE KILLING ME"
        sys.exit()
    except Exception, e:
        print e



