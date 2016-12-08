
import os, sys
import time

sys.path.append(os.getcwd())

import html_ops as ho

def writeTable( spots ):

    # Put the data in a table
    tabHtml = """
    <html>
        <head>
            <meta http-equiv="refresh" content="60" />
            <title>Lot Status</title>
            <script type="text/javascript" src="sorttable.js">
            </script>
            <style type="text/css">
            th, td {
              padding: 3px !important;
            }

            /* Sortable tables */
            table.sortable thead {
                background-color: #333;
                color: #cccccc;
                font-weight: bold;
                cursor: default;
            }
            th {
              font-size: 100%;
            }
            </style>
        </head>
        <table border="1" class="sortable">"""

    tabHtml += ("<tr><th>Space Number</th>"
                    "<th>Occupied</th>"
                    "<th>Time Present</th>"
                    "<th>Paid</th>"
                    "<th>Paid Start Time</th>"
                    "<th>Paid End Time</th>"
                    "<th>License Number</th>"
                    "<th>License State</th>"
                    "<th>Monthly</th>"
                    "<th>Occupation Start Time</th>"
                    "<th>Occupation End Time</th>"
                "</tr>")

    n_remaining = len(spots)
    
    # Make a separate table like normal, with paids only
    ptabHtml = tabHtml

    for s in spots:
        spot = spots[s]
        
        # Occupied once past presence threshold
        # -- Can be occupied and not paid for
        # -- duration of 'freeTime' or 'violationThresh'
        # -- before marked as violating.
        # -- Which is NOT what we want to indicate when
        # -- presenting the number of spots available
        occupied = spot['timeOccupied'] > 0
        deduct = occupied or spot['monthly']
        deduct = deduct or spot['faultyCamera']
        deduct = deduct or spot['handicap']

        n_remaining -= deduct
        
        # Default row to white
        rcolor = '#FFFFFF'

        # Black out if camera is failed
        if spot['faultyCamera']:
            rcolor = '#000000'

        if spot['violation']:
            rcolor = '#FF0000'
        elif spot['failedDetection']:
            rcolor = '#FF7F00'
        elif spot['monthly']:
            rcolor = '#0000FF'
        elif spot['paid']:
            rcolor = '#00FF00'
        elif spot['handicap']:
            rcolor = '#FFFF00'

        rowsty = 'style="background-color:%s"' % rcolor
        row = '<tr %s>' % rowsty
        
        spaceText = 'Space ' + str(s)
        linkText = '<a href="' + spot['url'] + '">' + spaceText + '</a>'
        spaceCell = '<td>' + linkText + '</td>'
        occCell = '<td> ' + str(occupied) + '</td>'
        presCell = '<td> ' + str(spot['timePresent']) + '</td>'
        paidCell = '<td> ' + str(spot['paid']) + '</td>'
        if spot['payStartTime']:
            pst_lt = time.localtime(spot['payStartTime'])
            pst_str = time.asctime(pst_lt)
        else:
            pst_str = ''
        if spot['payEndTime']:
            pet_lt = time.localtime(spot['payEndTime'])
            pet_str = time.asctime(pet_lt)
        else:
            pet_str = ''
        pstCell = '<td> ' + pst_str + '</td>'
        petCell = '<td> ' + pet_str + '</td>'
        lpnCell = '<td> ' + str(spot['lpn']) + '</td>'
        lpsCell = '<td> ' + str(spot['lps']) + '</td>'
        mnthCell = '<td> ' + str(spot['monthly']) + '</td>'
        ost_lt = time.localtime(spot['occupationStartTime'])
        oet_lt = time.localtime(spot['occupationEndTime'])
        ostCell = '<td> ' + time.asctime(ost_lt) + '</td>'
        oetCell = '<td> ' + time.asctime(oet_lt) + '</td>'
        row += spaceCell 
        row = row + occCell + presCell + paidCell
        row = row + pstCell + petCell
        row = row + lpnCell + lpsCell
        row += mnthCell
        row = row + ostCell + oetCell
        row += '</tr>'
        tabHtml += row
        
        # Only populate subtable with what's certain cases
        showMe = spot['paid'] == 1 or spot['violation']
        dontShowMe = spot['monthly']
        if showMe and not dontShowMe:
            ptabHtml += row

    
    endHtml = """
        </table>
    </html>"""

    tabHtml += endHtml
    ptabHtml += endHtml

    with open('table.html','w') as f:
        f.write(tabHtml)
    with open('paidTable.html','w') as f:
        f.write(ptabHtml)

    #os.rename("table.html","/var/www/html/newtable/index.html")
    #os.rename("paidTable.html","/var/www/html/whospaid/index.html")
    print 'WARNING: table webpage is not going to served site location!'

    nHtml = """\
            <div>
              <font size="7">
              %d
              </font>
            </div>
            """ % n_remaining 

    ho.write_page( 'n_avail.html', 'Available Spots', 30, nHtml )
    #os.rename("n_avail.html","/var/www/html/n_spots_available/index.html")
    print 'WARNING: number webpage is not going to served site location!'


    return

