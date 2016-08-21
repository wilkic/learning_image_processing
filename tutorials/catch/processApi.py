
import os, sys
import requests
import pprint as pp

sys.path.append(os.getcwd())

import send_mean as sm


import datetime as dt


import html_ops as ho

sys.path.append("..")
import notifications as notify

fails = 0

def assign_data( data, spots, monthlies ):
    
    if 'parkingRights' in data:
        paid = []
        for i in data['parkingRights']:
            sn = int( i['spaceNumber'] )
            paid += [sn]
            spots[ sn ]['paid'] = 1
            spots[ sn ]['payStartTime'] = str(i['startDateLocal'])
            spots[ sn ]['payEndTime'] = str(i['endDateLocal'])
            spots[ sn ]['lpn'] = str(i['lpn'])
            spots[ sn ]['lps'] = str(i['lpnState'])
        
        for s,spot in spots.iteritems():
            if s not in paid and s not in monthlies:
                spot['paid'] = 0

    return


def processApi( logdir, spots, monthlies, to ):

    global fails

    # Get the PM API response
    url = 'https://api.parkmobile.us/nforceapi/parkingrights/zone/3125?format=json'
    usr = 'ws_goodspeedcapi'
    pwd = 'x2warEya'
    
    i = 0
    while True:
        try:
            resp = requests.get(url, auth=(usr,pwd), verify=True)
            break
        except Exception, e:
            i += 1
            print 'BAD NEWS PARKMOBILE!'
            print 'Error number %d' % (i)
            if i==5:
                msg = """
                %s
                Park Mobile API is not responding!
                """ % dt.datetime.now()
                notify.send_msg('Error',msg,to)
                fails += 1
                if fails == 5:
                    raise

    # Populate spots based on response
    if resp.status_code != 404:
        try:
            # Read data
            data = resp.json()
            
            # Log it
            with open(os.path.join(logdir,'pmAPI.log'),'a') as out:
                print >> out, dt.datetime.now()
                pp.pprint( data, stream=out )
            
            # Write it to spot object
            assign_data( data, spots, monthlies )

        except Exception, e:
            print "PM API returning crap JSON?"
            print "Exception: \n%s" % str(e)
            print "Response: \n%s" % resp.text

    return

