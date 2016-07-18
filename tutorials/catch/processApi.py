
import ipdb

import os, sys

sys.path.append(os.getcwd())
import send_mean as sm

import pprint as pp

import datetime as dt

import requests

import html_ops as ho

def processApi( spots ):


    # Get the PM API response
    url = 'https://api.parkmobile.us/nforceapi/parkingrights/zone/3125?format=json'
    usr = 'ws_goodspeedcapi'
    pwd = 'x2warEya'
    resp = requests.get(url, auth=(usr,pwd), verify=True)

    # Populate spots based on response
    if resp.status_code != 404:
        data = resp.json()
        
        with open('pmAPI.log','a') as out:
            print >> out, dt.datetime.now()
            pp.pprint( data, stream=out )

        for i in data['parkingRights']:
            sn = int( i['spaceNumber'] )
            spots[ sn ]['paid'] = 1
            spots[ sn ]['payStartTime'] = str(i['startDateLocal'])
            spots[ sn ]['payEndTime'] = str(i['endDateLocal'])
            spots[ sn ]['lpn'] = str(i['lpn'])
            spots[ sn ]['lps'] = str(i['lpnState'])

    return

