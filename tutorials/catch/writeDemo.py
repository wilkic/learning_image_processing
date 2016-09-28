
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
                    "<th>Occupation Start Time</th>"
                    "<th>Occupation End Time</th>"
                "</tr>")

    dspots = [12, 13, 14]

    for s in spots:
        if s not in dspots:
            continue

        spot = spots[s]
        
        # Occupied once past presence threshold
        # -- Can be occupied and not paid for
        # -- duration of 'freeTime' or 'violationThresh'
        # -- before marked as violating.
        # -- Which is NOT what we want to indicate when
        # -- presenting the number of spots available
        occupied = spot['timeOccupied'] > 0
        n_remaining -= ( occupied ) 
        
        rcolor = '#FFFFFF'
        #if spot['violation']:
        #    rcolor = '#FF0000"'
        #elif spot['failedDetection']:
        #    rcolor = '#FF7F00"'
        #elif spot['paid'] == 1:
        #    rcolor = '#00FF00"'
        #elif spot['paid']:
        #    rcolor = '#0000FF"'

        rowsty = 'style="background-color:%s"' % rcolor
        row = '<tr %s>' % rowsty
        
        spaceText = 'Space ' + str(s)
        linkText = '<a href="' + spot['url'] + '">' + spaceText + '</a>'
        spaceCell = '<td>' + linkText + '</td>'
        occCell = '<td> ' + str(occupied) + '</td>'
        presCell = '<td> ' + str(spot['timePresent']) + '</td>'
        ost_lt = time.localtime(spot['occupationStartTime'])
        oet_lt = time.localtime(spot['occupationEndTime'])
        ostCell = '<td> ' + time.asctime(ost_lt) + '</td>'
        oetCell = '<td> ' + time.asctime(oet_lt) + '</td>'
        row += spaceCell 
        row = row + occCell + presCell
        row = row + ostCell + oetCell
        row += '</tr>'
        tabHtml += row
        
    endHtml = """
        </table>
    </html>"""

    tabHtml += endHtml
    
    tabFname = 'demotable.html'
    with open(tabFname,'w') as f:
        f.write(tabHtml)

    #os.rename(tabFname,"/var/www/html/demotable/index.html")
    #print 'WARNING: number webpage is not going to served site location!'


    return

