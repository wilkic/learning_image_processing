
import ipdb

import os, sys

sys.path.append(os.getcwd())
import send_mean as sm

import pprint as pp

import datetime as dt

import requests

import html_ops as ho

def processApi( logdir, spots ):


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
                raise

    # Populate spots based on response
    if resp.status_code != 404:
        data = resp.json()
        

        with open(os.path.join(logdir,'pmAPI.log'),'a') as out:
            print >> out, dt.datetime.now()
            pp.pprint( data, stream=out )
        
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
            if s not in paid:
                spot['paid'] = 0

    return

