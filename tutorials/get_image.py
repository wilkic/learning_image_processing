
import os
import sys
import datetime as dt
import notifications as notify
from shutil import copyfile

def get_image( ip, cam, fname, wd, to ):
    

    # store snapshot to processing dir (wd)
    # using wget cuz otherwise I can't open the file (urllib etc)
    url = 'http://' + ip + ':' + str(cam['port'])
    url += '/cgi-bin/getsnapshot.cgi'
    call = 'wget ' + url + ' -O ' + fname + ' >/dev/null 2>&1'
    # Verbose
    #call = 'wget ' + url + ' -O ' + fname
    
    tries = 0
    while True:
        if tries>10:
            msg = """
            %s
            Camera %d is not producing images !
            """ % (str(dt.datetime.now()),cam['number'])
            notify.send_msg(msg,to)
            print msg   
            sys.exit()

        tries += 1
        os.system(call)
        if os.stat(fname).st_size < 16000:
            copyfile(fname, wd+'/failed_snap_'+str(tries)+'.jpg')
            continue
        else:
            break

    
    # get timestamp
    ts = dt.datetime.now()
    
    # get time since last image
    delta_time_obj = ts - cam['im_ts']
    delta_time = delta_time_obj.total_seconds()
    
    # set timestamp for current image
    cam['im_ts'] = ts

    return delta_time

