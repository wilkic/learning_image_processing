
import sys
import os
from shutil import copyfile

sys.path.append(os.getcwd())
import dataRecording as log
import analyzeImage as ai
import determinePresence as dp
import evaluatePresence as ep

sys.path.append("..")
import notifications as notify
import get_image as gi

####

def processCameras( ip, cameras, dirs, to ):
    
    for c, camera in cameras.iteritems():
        
        # Write jpeg to image dir and
        # populate camera dict with time info
        result = gi.get_image( ip, camera, dirs['wd'], to )
        
        if result['success']:
            delta_time = result['delta_time']
            fname = result['fname']
            
            # Process image
            ai.analyzeImage( fname, camera ) 

            # Judging
            for spot in camera['spots']:

                present = dp.determinePresence( spot )
                
                msg = ep.evaluatePresence( spot,
                                           present,
                                           delta_time,
                                           camera['im_ts'] )
                
                if msg is not None:
                    notify.send_msg_with_jpg( msg, fname, to )
                
                # Store all current images
                sfname = 'spot' + str(spot['number']) + '.jpg'
                cfname = os.path.join( dirs['cd'], sfname )
                copyfile(fname,cfname)

                # Log spot data
                log.logSpot( camera['im_ts'], spot, dirs['sld'] )

            # reset failure counter
            camera['nFails'] = 0
            
            # delete the image that has been processed
            os.remove(fname)

        else:
            camera['nFails'] += 1
            
            if camera['nFails'] == 5:
                msg = """
                %s
                Camera %d is not producing images !
                """ % (time.asctime(),camera['number'])
                notify.send_msg(msg,to)
                print msg
            

        # store the current state of the camera
        #log.addState( camera, dirs['cld'] )
        log.recordState( camera, dirs['csd'] )

    return

