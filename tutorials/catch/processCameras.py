
import sys
import os
from shutil import copyfile
import time

sys.path.append(os.getcwd())
import dataRecording as log
import analyzeImage as ai
import determinePresence as dp
import evaluatePresence as ep

sys.path.append("..")
import notifications as notify
import get_image as gi

####
def useImage( camera, imDir ):
    
    # set image filename
    fname = imDir + '/cam' + str(camera['number']) + '.jpg';
    
    # if file is there... we're good
    # TODO... need to check that file is current
    success = os.path.exists(fname)

    # get current time
    ts = time.time()
    
    # get time since last image
    delta_time = ts - camera['im_ts']

    # set timestamp for current image
    camera['im_ts'] = ts

    result = {'success': success,
              'fname': fname,
              'delta_time': delta_time}
    
    return result

def processCameras( cameras, dirs, to, spam=None ):
    
    for c, camera in cameras.iteritems():
        
        ## Write jpeg to image dir and
        ## populate camera dict with time info
        #result = gi.get_image( camera, dirs['wd'] )
        
        # Use images already popped into server
        result = useImage( camera, dirs['pd'] )
        
        if result['success']:
            delta_time = result['delta_time']
            fname = result['fname']
            
            # Process image
            ai.analyzeImage( fname, camera ) 

            # Judging
            for spot in camera['spots']:

                present = dp.determinePresence( spot )
                
                res = ep.evaluatePresence( spot,
                                           present,
                                           delta_time,
                                           camera['im_ts'] )
                if res['message'] is not None and spam is not None:
                    notify.send_msg_with_jpg( res['subject'],
                                              res['message'],
                                              fname, spam )
                
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
                notify.send_msg('Error',msg,to)
                print msg
            
            # Protect against giant seepage
            if camera['nFails'] > 100:
                camera['nFails'] = 100
            

        # store the current state of the camera
        #log.addState( camera, dirs['cld'] )
        log.recordState( camera, dirs['csd'] )

    return

