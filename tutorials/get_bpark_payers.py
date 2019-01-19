#!/usr/bin/env python

import os, sys

sys.path.append(os.getcwd())
import send_mean as sm

import pprint as pp

import datetime as dt

import requests

import html_ops as ho


# Number of available spots
nSpots = 16
nPaidSpots = 0

# Get the PM API response
zone = 3127
url = 'https://api.parkmobile.us/nforceapi/parkingrights/zone/%s?format=json' % zone
usr = 'ws_goodspeedcapi'
pwd = 'x2warEya'
resp = requests.get(url, auth=(usr,pwd), verify=True)


# Make a header row for table of data from API call
tabHtml = '<table border="1">'
tabHtml += ("<tr><td>Paid Start Time</td>"
                "<td>Paid End Time</td>"
                "<td>License Number</td>"
                "<td>License State</td>"
            "</tr>")

# Parse API response JSON
if resp.status_code != 404:
    data = resp.json()
    
    # Default row to white
    rcolor = '#FFFFFF'
    rowsty = 'style="background-color:%s"' % rcolor
    
    # Populate row of table from API response
    for i in data['parkingRights']:
    
        row = '<tr %s>' % rowsty
        pstCell = '<td> ' + str(i['startDateLocal']) + '</td>'
        petCell = '<td> ' + str(i['endDateLocal']) + '</td>'
        lpnCell = '<td> ' + str(i['lpn']) + '</td>'
        lpsCell = '<td> ' + str(i['lpnState']) + '</td>'
        row = row + pstCell + petCell
        row = row + lpnCell + lpsCell
        row += '</tr>'
        tabHtml += row

        nPaidSpots += 1


    # Log raw API results 
    #outdir = '/mnt/data/catch/bpark/get_payer_output'
    outdir = '/tmp/get_payer_output'

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    outfile = os.path.join(outdir,'bp_pmAPI.log')

    with open(outfile,'a') as out:
        print >> out, dt.datetime.now()
        pp.pprint( data, stream=out )


# Finish the table
tabHtml += '</table>'

# Write the full page html
ho.write_page( 'bpark_table.html', 'Paid Spots', 60, tabHtml )

# Move it to the right spot
#os.rename("bpark_table.html","/var/www/html/bpark/table/index.html")
os.rename("bpark_table.html","/tmp/bptab.html")

######################

# How many unpaid spots remain
n_remaining = nSpots - nPaidSpots

nHtml = """\
        <div>
          <font size="7">
          %d
          </font>
        </div>
        """ % n_remaining 

ho.write_page( 'n_bpark_avail.html', 'Available Spots', 300, nHtml )
#os.rename("n_bpark_avail.html","/var/www/html/bpark/n_spots_not_paid/index.html")
os.rename("n_bpark_avail.html","/tmp/nsnp.html")


