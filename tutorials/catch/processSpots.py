from shutil import copyfile
import time

import os, sys
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
        'occupationEndTime': 0,
        'violation': False,
        'failedDetection': False,
    }

    spots = {prop:defaultProperties.copy() for prop in range(1,nSpots+1)}

    # Assign the monthlies
    for i in monthlies:
        spots[i]['monthly'] = 1
        spots[i]['paid'] = 0.9

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

def judge( spots, freeTime, to, imdir, vdir, udir ):

    for s, spot in spots.iteritems():

        if spot['timeOccupied'] > freeTime and not spot['paid']:
            if not spot['violation']:

                spot['violation'] = True
                
                lt = time.localtime(spot['occupationStartTime'])
                tss = time.strftime('%Y%m%dT%H%M%S',lt)
                
                ss = str(s)
                fname = 'spot' + ss + '.jpg'
                fname = os.path.join( imdir, fname )
                vfname = 'spot' + ss + '_' + tss + '.jpg'
                vfname = os.path.join( vdir, vfname )
                copyfile( fname, vfname ) 
                sub = "Violation"
                msg = """
                %s
                Spot %d in VIOLATION
                """ % (time.asctime(lt), s)
                notify.send_msg_with_jpg( sub, msg, vfname, to )
        else:
            spot['violation'] = False
            
            if spot['paid'] == 1 and spot['timePresent'] == 0:
                pss = spot['payStartTime']
                pstt = time.strptime(pss[0:19],"%Y-%m-%dT%H:%M:%S")
                pst = time.mktime(pstt)
                pes = spot['payEndTime']
                pett = time.strptime(pes[0:19],"%Y-%m-%dT%H:%M:%S")
                pet = time.mktime(pett)
                
                oet = spot['occupationEndTime']

                if oet < pst :
                    if not spot['failedDetection']:
                        spot['failedDetection'] = True

                        tss = spot['payStartTime']

                        ss = str(s)
                        fname = 'spot' + ss + '.jpg'
                        fname = os.path.join( imdir, fname )
                        ufname = 'spot' + ss + '_' + tss + '.jpg'
                        ufname = os.path.join( udir, ufname )
                        copyfile( fname, ufname ) 
                        sub = "Failed Detection?"
                        msg = """
                        %s
                        Spot %d Detection Failed, or ...
                        Person left spot within pay period
                        """ % (tss, s)
                        notify.send_msg_with_jpg( sub, msg, ufname, to )
                else:
                    spot['failedDetection'] = False
            else:
                spot['failedDetection'] = False

    return
