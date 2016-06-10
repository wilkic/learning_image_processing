#!/usr/bin/env python

import os, sys
#sys.path.append('/home/project')
import send_mean as sm

#import requests
#url = 'https://api.parkmobile.us/nforceapi/parkingrights/zones/1/99999?format=json'
#usr = 'ws_cobbgoodspeed'
#pwd = 'P@rkmobile1'
#resp = requests.get(url, auth=(usr,pwd), verify=True)
#
#data = resp.json()

resp = {"resultTimeStampLocal":"\"2016-06-07T18:26:07.7759835\"","parkingRights":[{"parkingRightId":65528390,"signageZoneCode":"9911","internalZoneCode":"9911","supplierId":993099,"lpn":"PMTEST","lpnState":"GA","startDateLocal":"2016-06-07T18:18:01.4230000","endDateLocal":"2016-06-07T20:18:01.4230000","productDescription":"Cashless Parking","spaceNumber":"","timeZone":"Eastern Standard Time","permit":"","modifiedDate":"2016-06-07T18:18:04.9400000","payedMinutes":120,"purchaseAmount":2.00,"productTypeId":1}],"totalCount":1,"resultCount":1}

N_paid_cars = resp['totalCount']

check = len( resp['parkingRights'] )

if N_paid_cars != check:
    err = 'API result not self consistent:\n'\
          'totalCount = ' + N_paid_cars + '\n'\
          'number of parkingRights = ' + check + '\n'

    sm.send_msg( err )

nSpots = 5

spots = {prop:{'pd':0,'occ':0} for prop in range(1,nSpots+1)}

for i in resp['parkingRights']:
    if i['spaceNumber']:
        sn = int( i['spaceNumber'] )
        spots[ sn ]['pd'] = 1

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
            "</tr>")

              
for spot in spots:
    row = '<tr>'
    spaceCell = '<td>Space ' + str(spot) + '</td>'
    occCell = '<td> ' + str(spots[spot]['occ']) + '</td>'
    paidCell = '<td> ' + str(spots[spot]['pd']) + '</td>'
    row = row + spaceCell + occCell + paidCell
    row += '</tr>'
    tabHtml += row

tabHtml += '</table>'

headHtml = '<head><meta http-equiv="refresh" content="30" />'
headHtml += '<title>Lot Status</title></head>'

pageHtml = '<html>'
pageHtml += headHtml
pageHtml += tabHtml + '</html>'

fido = open('table.html','w')
fido.write(pageHtml)
fido.close()



os.rename("table.html","/var/www/html/table/index.html")

