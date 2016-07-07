#!/usr/bin/env python

import os
import sys
import datetime as dt

#################################
#################################
#################################

#ip = 192.168.1.154
#port = None

ip = '108.45.109.111'

bd = 'camera'
bport = 9000

cams = range(1,16)

store_dir = '/home/acp/Projects/ggp/cam_images'

#################################
#################################
#################################

for c in cams:

    d = bd + str(c)
    port = bport + c

    wd = os.path.join( store_dir, d )
    if not os.path.exists(wd):
        os.makedirs(wd)

    ts = dt.datetime.now()
    tss = ts.strftime('%Y%m%d%H%M%S')

    fname = wd + '/snap' + tss + '.jpg'

    url = 'http://' + ip
    if port is not None:
        url += ':' + str(port)

    url += '/cgi-bin/getsnapshot.cgi'
    #call = 'wget ' + url + ' -O ' + fname + ' >/dev/null 2>&1'
    call = 'wget ' + url + ' -O ' + fname

    tries = 0
    while True:
        if tries>10:
            msg = """
            %s
            Camera is not producing images !
            """ % tss
            print msg
            sys.exit()

        tries += 1
        os.system(call)
        if os.stat(fname).st_size < 16000:
            continue
        else:
            break


