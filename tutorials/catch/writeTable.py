
import ipdb

import os, sys

sys.path.append(os.getcwd())

import html_ops as ho

def writeTable( spots ):

    # Put the data in a table
    tabHtml = '<table border="1">'
    tabHtml += ("<tr><td>Space Number</td>"
                    "<td>Occupied</td>"
                    "<td>Time Present</td>"
                    "<td>Paid</td>"
                    "<td>Paid Start Time</td>"
                    "<td>Paid End Time</td>"
                    "<td>License Number</td>"
                    "<td>License State</td>"
                    "<td>Monthly</td>"
                    "<td>Occupation Start Time</td>"
                    "<td>Occupation End Time</td>"
                "</tr>")


    n_remaining = len(spots)

    for spot in spots:

        # For now, update remaining number of
        # spots based on the number paid
        n_remaining -= spots[spot]['paid']

        row = '<tr>'
        spaceCell = '<td>Space ' + str(spot) + '</td>'
        occCell = '<td> ' + str(spots[spot]['timeOccupied']>0) + '</td>'
        presCell = '<td> ' + str(spots[spot]['timePresent']) + '</td>'
        paidCell = '<td> ' + str(spots[spot]['paid']) + '</td>'
        pstCell = '<td> ' + str(spots[spot]['payStartTime']) + '</td>'
        petCell = '<td> ' + str(spots[spot]['payEndTime']) + '</td>'
        lpnCell = '<td> ' + str(spots[spot]['lpn']) + '</td>'
        lpsCell = '<td> ' + str(spots[spot]['lps']) + '</td>'
        mnthCell = '<td> ' + str(spots[spot]['monthly']) + '</td>'
        ostCell = '<td> ' + str(spots[spot]['occupationStartTime']) + '</td>'
        oetCell = '<td> ' + str(spots[spot]['occupationEndTime']) + '</td>'
        row += spaceCell 
        row = row + occCell + presCell + paidCell
        row = row + pstCell + petCell
        row = row + lpnCell + lpsCell
        row = row + ostCell + oetCell
        row += mnthCell
        row += '</tr>'
        tabHtml += row

    tabHtml += '</table>'

    ho.write_page( 'table.html', 'Lot Status', 15, tabHtml )
    #os.rename("table.html","/var/www/html/table/index.html")
    print 'WARNING: table webpage is not going to served site location!'

    nHtml = """\
            <div>
              <font size="7">
              %d
              </font>
            </div>
            """ % n_remaining 

    ho.write_page( 'n_avail.html', 'Available Spots', 15, nHtml )
    #os.rename("n_avail.html","/var/www/html/n_spots_available/index.html")
    print 'WARNING: number webpage is not going to served site location!'


    return

