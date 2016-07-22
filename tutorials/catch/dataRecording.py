
import os
import csv
import pprint as pp

####

def setupDirs( baseDir ):
    sld = os.path.join( baseDir, 'spot_logs' )
    if not os.path.exists(sld):
        os.makedirs(sld)

    # Put camera logs in their own dir
    cld = os.path.join( baseDir, 'camera_logs' )
    if not os.path.exists(cld):
        os.makedirs(cld)

    # Put camera states in their own dir
    csd = os.path.join( baseDir, 'camera_states' )
    if not os.path.exists(csd):
        os.makedirs(csd)
    
    return sld, cld, csd


def logSpot( ts, spot, logDir ):
    
    # Log spot data
    data = ( [ts, spot['timePresent']] 
             + spot['means']
             + spot['sigs']
             + spot['maxs']
             + spot['mins']
             + [spot['nEdges']]
             + [spot['nKeys']] )

    fname = 'spot' + str(spot['number']) + '.log'
    ffname = os.path.join( logDir, fname )
    
    with open(ffname,'a+') as l:
        w = csv.writer(l)
        w.writerow(data)
    
    return

def addState( camera, logDir ):
    
    # append the state to the log
    fname = 'camera' + str(camera['number']) + '_dict.log'
    ffname = os.path.join(logDir,fname)
    with open(ffname,'a+') as out:
        pp.pprint( camera, stream=out )
    
    return

def recordState( camera, logDir ):

    # store the current state of the camera
    fname = 'camera' + str(camera['number']) + '.dict'
    ffname = os.path.join( logDir, fname )
    with open(ffname,'w+') as out:
        pp.pprint( camera, stream=out )
    
    return

