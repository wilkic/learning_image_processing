#!/usr/bin/env python

import ipdb

import os, sys

sys.path.append(os.getcwd())
import send_mean as sm

import pprint as pp

import datetime as dt

import requests

import html_ops as ho


# Set up the spots dictionary
nSpots = 49

# These spots are monthly
monthlies = [10, 11, 12, 13, 14, 35, 36, 37, 38, 39, 40, 41, 42]

defaultProperties = {
    'paid': 0,
    'occupied': 0,
    'startTime': '',
    'endTime': '',
    'lps': '',
    'lpn': '',
    'monthly': 0
}

spots = {prop:defaultProperties.copy() for prop in range(1,nSpots+1)}

# Assign the monthlies
for i in monthlies:
    spots[i]['monthly'] = 1
    spots[i]['paid'] = 1


# Get the PM API response
url = 'https://api.parkmobile.us/nforceapi/parkingrights/zone/3125?format=json'
usr = 'ws_goodspeedcapi'
pwd = 'x2warEya'
resp = requests.get(url, auth=(usr,pwd), verify=True)

# Populate spots based on response
if resp.status_code != 404:
    data = resp.json()
    
    with open('/mnt/data/catch/get_car_data_pmAPI.log','a') as out:
        print >> out, dt.datetime.now()
        pp.pprint( data, stream=out )

    for i in data['parkingRights']:
        sn = int( i['spaceNumber'] )
        if sn <= len(spots):
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
                "<td>Monthly</td>"
            "</tr>")


n_remaining = nSpots

for spot in spots:

    # For now, update remaining number of
    # spots based on the number paid
    n_remaining -= spots[spot]['paid']

    row = '<tr>'
    spaceCell = '<td>Space ' + str(spot) + '</td>'
    occCell = '<td> ' + str(spots[spot]['occupied']) + '</td>'
    paidCell = '<td> ' + str(spots[spot]['paid']) + '</td>'
    pstCell = '<td> ' + str(spots[spot]['startTime']) + '</td>'
    petCell = '<td> ' + str(spots[spot]['endTime']) + '</td>'
    lpnCell = '<td> ' + str(spots[spot]['lpn']) + '</td>'
    lpsCell = '<td> ' + str(spots[spot]['lps']) + '</td>'
    mnthCell = '<td> ' + str(spots[spot]['monthly']) + '</td>'
    row += spaceCell 
    row = row + occCell + paidCell
    row = row + pstCell + petCell
    row = row + lpnCell + lpsCell
    row += mnthCell
    row += '</tr>'
    tabHtml += row

tabHtml += '</table>'

ho.write_page( 'table.html', 'Lot Status', 15, tabHtml )
os.rename("table.html","/var/www/html/table/index.html")

nHtml = """\
        <div>
          <font size="7">
          %d
          </font>
        </div>
        """ % n_remaining 

ho.write_page( 'n_avail.html', 'Available Spots', 15, nHtml )
os.rename("n_avail.html","/var/www/html/n_spots_not_paid/index.html")


