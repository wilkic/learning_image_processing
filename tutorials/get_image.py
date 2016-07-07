
import os
import sys
import datetime as dt
from shutil import copyfile

def get_image( ip, cam, wd, to ):
    
    # File name of image in working dir while processing
    fname = wd + '/snap.jpg'

    # store snapshot to processing dir (wd)
    # using wget cuz otherwise I can't open the file (urllib etc)
    url = 'http://' + ip + ':' + str(cam['port'])
    url += '/cgi-bin/getsnapshot.cgi'
    fout = ' -O ' + fname + ' '
    timeout = ' --timeout=5 --tries=2'
    dump = ' >/dev/null 2>&1'
    call = 'wget ' + url + fout  + timeout + dump
    # Verbose
    #call = 'wget ' + url + ' -O ' + fname
    
    tries = 0
    success = True
    while True:
        if tries>10:
            success = False
            break

        tries += 1
        os.system(call)
        if os.path.isfile(fname):
            if os.stat(fname).st_size < 16000:
                copyfile(fname, wd+'/failed_snap_'+str(tries)+'.jpg')
                continue
            else:
                break
        else:
            continue

    
    # get timestamp
    ts = dt.datetime.now()
    
    # get time since last image
    delta_time_obj = ts - cam['im_ts']
    delta_time = delta_time_obj.total_seconds()
    
    # set timestamp for current image
    cam['im_ts'] = ts
    
    result = {'success': success,
              'fname': fname,
              'delta_time': delta_time}
    
    return result

