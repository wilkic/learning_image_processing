#!/usr/bin/env python

import ipdb

import os, sys
#sys.path.append('/home/project')
import send_mean as sm

import requests
url = 'https://api.parkmobile.us/nforceapi/parkingrights/zone/3125?format=json'
usr = 'ws_goodspeedcapi'
pwd = 'x2warEya'
resp = requests.get(url, auth=(usr,pwd), verify=True)

data = resp.json()

#data = {"resultTimeStampLocal":"\"2016-06-07T18:26:07.7759835\"","parkingRights":[{"parkingRightId":65528390,"signageZoneCode":"9911","internalZoneCode":"9911","supplierId":993099,"lpn":"PMTEST","lpnState":"GA","startDateLocal":"2016-06-07T18:18:01.4230000","endDateLocal":"2016-06-07T20:18:01.4230000","productDescription":"Cashless Parking","spaceNumber":"","timeZone":"Eastern Standard Time","permit":"","modifiedDate":"2016-06-07T18:18:04.9400000","payedMinutes":120,"purchaseAmount":2.00,"productTypeId":1}],"totalCount":1,"resultCount":1}

N_paid_cars = data['totalCount']

check = len( data['parkingRights'] )

if N_paid_cars != check:
    err = 'API result not self consistent:\n'\
          'totalCount = ' + N_paid_cars + '\n'\
          'number of parkingRights = ' + check + '\n'

    sm.send_msg( err )

nSpots = 49

defaultProperties = {
    'paid': 0,
    'occupied': 0,
    'startTime': '',
    'endTime': '',
    'lps': '',
    'lpn': ''
}

spots = {prop:defaultProperties.copy() for prop in range(1,nSpots+1)}

for i in data['parkingRights']:
    ipdb.set_trace()
    sn = int( i['spaceNumber'] )
    spots[ sn ]['paid'] = 1
    spots[ sn ]['startTime'] = str(i['startDateLocal'])
    spots[ sn ]['endTime'] = str(i['endDateLocal'])
    spots[ sn ]['lpn'] = str(i['lpn'])
    spots[ sn ]['lps'] = str(i['lpnState'])


# TODO:
# * Call VIPER to get the occupied status
# * Perform check against paid, notify if mismatch
#  * Call send_mail, send_sms
#  * Probably need a persistence (use timestamps from images and PM)


# Put the data in a table
tabHtml = '<table border="1">'
tabHtml += ("<tr><td>Space Number</td>"
                "<td>Occupied</td>"
                "<td>Paid</td>"
                "<td>Paid Start Time</td>"
                "<td>Paid End Time</td>"
                "<td>License Number</td>"
                "<td>License State</td>"
            "</tr>")

              
for spot in spots:
    row = '<tr>'
    spaceCell = '<td>Space ' + str(spot) + '</td>'
    occCell = '<td> ' + str(spots[spot]['occupied']) + '</td>'
    paidCell = '<td> ' + str(spots[spot]['paid']) + '</td>'
    pstCell = '<td> ' + str(spots[spot]['startTime']) + '</td>'
    petCell = '<td> ' + str(spots[spot]['endTime']) + '</td>'
    lpnCell = '<td> ' + str(spots[spot]['lpn']) + '</td>'
    lpsCell = '<td> ' + str(spots[spot]['lps']) + '</td>'
    row += spaceCell 
    row = row + occCell + paidCell
    row = row + pstCell + petCell
    row = row + lpnCell + lpsCell
    row += '</tr>'
    tabHtml += row

tabHtml += '</table>'

headHtml = '<head><meta http-equiv="refresh" content="3" />'
headHtml += '<title>Lot Status</title></head>'

pageHtml = '<html>'
pageHtml += headHtml
pageHtml += tabHtml + '</html>'

fido = open('table.html','w')
fido.write(pageHtml)
fido.close()



os.rename("table.html","/var/www/html/table/index.html")

