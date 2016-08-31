#!/usr/bin/env python

import ipdb

import os, sys

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
url = 'https://api.parkmobile.us/nforceapi/parkingrights/zone/3125?format=jso://ppprk.com/apps/v7/server/opmgmt/api/partner_index.php/getzoneinfo?format=json'
zoneId = 476823
apiKey = 'cde94f0cb408435d9792da3d525a9671'
fullUrl = url + '&apikey=' + apiKey + '&zoneid=' str(zoneId)

resp = requests.get(fullUrl)

# Populate spots based on response
if resp.status_code != 404:
    data = resp.json()
    data = data['data'][0]

    with open('paymentAPI.log','a') as out:
        print >> out, dt.datetime.now()
        pp.pprint( data, stream=out )

    for i in data['spaces']:
        sn = int( i['number'] )
        spots[ sn ]['paid'] = 1
        spots[ sn ]['startTime'] = str(i['entrytime'])
        spots[ sn ]['endTime'] = str(i['exittime'])

# Put the data in a table
tabHtml = '<table border="1">'
tabHtml += ("<tr><td>Space Number</td>"
                "<td>Occupied</td>"
                "<td>Paid</td>"
                "<td>Paid Start Time</td>"
                "<td>Paid End Time</td>"
                "<td>Monthly</td>"
            "</tr>")


n_remaining = nSpots

for spot in spots:

    # For now, update remaining number of
    # spots based on the number paid
    n_remaining -= spots[spot]['paid']

    row = '<tr>'
    spaceCell = '<td>Space ' + str(spot) + '</td>'
    paidCell = '<td> ' + str(spots[spot]['paid']) + '</td>'
    pstCell = '<td> ' + str(spots[spot]['startTime']) + '</td>'
    petCell = '<td> ' + str(spots[spot]['endTime']) + '</td>'
    mnthCell = '<td> ' + str(spots[spot]['monthly']) + '</td>'
    row += spaceCell 
    row = row + occCell + paidCell
    row = row + pstCell + petCell
    row = row + lpnCell + lpsCell
    row += mnthCell
    row += '</tr>'
    tabHtml += row

tabHtml += '</table>'

ho.write_page( 'table.html', 'Lot Status', 60, tabHtml )
os.rename("table.html","/var/www/html/table/index.html")

nHtml = """\
        <div>
          <font size="7">
          %d
          </font>
        </div>
        """ % n_remaining 

ho.write_page( 'n_avail.html', 'Available Spots', 15, nHtml )
os.rename("n_avail.html","/var/www/html/n_spots_available/index.html")


