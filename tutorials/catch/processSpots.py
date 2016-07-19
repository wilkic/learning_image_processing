import time

import sys
sys.path.append("..")
import notifications as notify

def create( nSpots, monthlies ):

    # Set up the spots dictionary
    nSpots = 49

    # These spots are monthly
    monthlies = [39, 40, 41, 42]

    defaultProperties = {
        'paid': 0,
        'payStartTime': '',
        'payEndTime': '',
        'lps': '',
        'lpn': '',
        'monthly': 0,
        'timePresent': 0,
        'timeOccupied': 0,
        'occupationStartTime': 0,
        'occupationEndTime': 0
    }

    spots = {prop:defaultProperties.copy() for prop in range(1,nSpots+1)}

    # Assign the monthlies
    for i in monthlies:
        spots[i]['monthly'] = 1
        spots[i]['paid'] = 1

    return spots

def write( cameras, spots ):
    
    for c, camera in cameras.iteritems():
        
        for spot in camera['spots']:
            
            sn = spot['number']
            spots[sn]['timePresent'] = spot['timePresent']
            spots[sn]['timeOccupied'] = spot['timeOccupied']
            spots[sn]['occupationStartTime'] = spot['occupationStartTime']
            spots[sn]['occupationEndTime'] = spot['occupationEndTime']
    
    return

def judge( spots, freeTime, to, imdir, vdir ):

    for s, spot in spots.iteritems():

        if spot['timeOccupied'] > freeTime:
           if spot['paid'] < 1:
                spot['violation'] = True
                
                gmt = time.gmtime(spot['occupationStartTime'])
                tss = time.asctime(gmt)

                fname = 'spot' + s + '.jpg'
                fname = os.path.join( imdir, fname )
                vfname = 'spot' + s + '_' + tss + '.jpg'
                vfname = os.path.join( vdir, vfname )
                copyfile( fname, vfname ) 
                msg = """
                %s
                Spot %d in VIOLATION
                """ % (time.asctime(), s)
                notify.send_msg_with_jpg( msg, vfname, to )

    
    return
