#!/usr/bin/env python

import ipdb

import os, sys
import time
import pprint as pp

sys.path.append(os.getcwd())

import requests

import html_ops as ho


# Set up the spots dictionary
spotNumbers = range(1001,1119+1) + range(1127,1132+1)


# These spots are monthly
monthlies = []

defaultProperties = {
    'paid': 0,
    'occupied': 0,
    'startTime': '',
    'endTime': '',
    'monthly': 0
}

spots = {prop:defaultProperties.copy() for prop in spotNumbers}

# Assign the monthlies
for i in monthlies:
    spots[i]['monthly'] = 1
    spots[i]['paid'] = 1


# Get the API response
url = 'https://ppprk.com/apps/v7/server/opmgmt/api/partner_index.php/getzoneinfo?format=json'
zoneId = 476823
apiKey = 'cde94f0cb408435d9792da3d525a9671'
fullUrl = url + '&apikey=' + apiKey + '&zoneid=' + str(zoneId)

resp = requests.get(fullUrl)

# Populate spots based on response
if resp.status_code != 404:
    data = resp.json()
    data = data['data'][0]

    with open('paymentAPI.log','a') as out:
        print >> out, time.asctime()
        pp.pprint( data, stream=out )

    for i in data['locations_spaces'][0]['spaces']:
        sn = int( i['number'] )
        spots[ sn ]['paid'] = 1
        spots[ sn ]['startTime'] = str(i['formattedentrytime'])
        spots[ sn ]['endTime'] = str(i['formattedexittime'])

# Put the data in a table
tabHtml = '<table border="1">'
tabHtml += ("<tr><td>Space Number</td>"
                "<td>Paid</td>"
                "<td>Paid Start Time</td>"
                "<td>Paid End Time</td>"
                "<td>Monthly</td>"
            "</tr>")


n_remaining = len(spotNumbers)

ptabHtml = tabHtml

for s in spots:
    
    spot = spots[s]

    # For now, update remaining number of
    # spots based on the number paid
    
    rcolor = '#FFFFFF'
    if spot['paid']:
        n_remaining -= 1
        rcolor = '#00FF00'
    
    rowsty = 'style="background-color:%s"' % rcolor

    row = '<tr %s>' % rowsty

    spaceCell = '<td>Space ' + str(s) + '</td>'
    paidCell = '<td> ' + str(spot['paid']) + '</td>'
    pstCell = '<td> ' + str(spot['startTime']) + '</td>'
    petCell = '<td> ' + str(spot['endTime']) + '</td>'
    mnthCell = '<td> ' + str(spot['monthly']) + '</td>'
    row += spaceCell 
    row = row + paidCell
    row = row + pstCell + petCell
    row += mnthCell
    row += '</tr>'
    tabHtml += row

    if spot['paid']:
        ptabHtml += row

endHtml = """
</table"""

tabHtml += endHtml
ptabHtml += endHtml

tname = 'tablePassport.html'
ho.write_page( tname, 'Lot Status', 60, tabHtml )
#os.rename(tname,"/var/www/html/reston/table/index.html")

tname = 'paidtablePassport.html'
ho.write_page( tname, 'Lot Status', 60, ptabHtml )
#os.rename(tname,"/var/www/html/reston/whospaid/index.html")

nHtml = """\
        <div>
          <font size="7">
          %d
          </font>
        </div>
        """ % n_remaining 

nname = 'n_availPassport.html'
ho.write_page( nname, 'Available Spots', 60, nHtml )
#os.rename(nname,"/var/www/html/reston/n_spots_available/index.html")


