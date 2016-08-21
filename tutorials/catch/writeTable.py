
import ipdb

import os, sys
import time

sys.path.append(os.getcwd())

import html_ops as ho

def writeTable( spots ):

    # Put the data in a table
    tabHtml = """
    <html>
        <head>
            <meta http-equiv="refresh" content="30" />
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

        # For now, update remaining number of
        # spots based on the number paid
        n_remaining -= spot['paid']
        
        rcolor = '#FFFFFF'
        if spot['violation']:
            rcolor = '#FF0000"'
        elif spot['failedDetection']:
            rcolor = '#FF7F00"'
        elif spot['paid'] == 1:
            rcolor = '#00FF00"'
        elif spot['paid']:
            rcolor = '#0000FF"'

        rowsty = 'style="background-color:%s"' % rcolor
        row = '<tr %s>' % rowsty
        
        spaceText = 'Space ' + str(s)
        linkText = '<a href="' + spot['url'] + '">' + spaceText + '</a>'
        spaceCell = '<td>' + linkText + '</td>'
        occCell = '<td> ' + str(spot['timeOccupied']>0) + '</td>'
        presCell = ( '<td class="timp"> '
                     + str(spot['timePresent'])
                     + '</td>' )
        paidCell = ( '<td class="pd"> '
                     + str(spot['paid'])
                     + '</td>' )
        rpst_str = str(spot['payStartTime'])
        rpet_str = str(spot['payEndTime'])
        if not rpst_str:
            pstCell = '<td> </td>'
        else:
            pstt = time.strptime(rpst_str[0:19],"%Y-%m-%dT%H:%M:%S")
            pstCell = '<td> ' + time.asctime(pstt) + '</td>'
        if not rpet_str:
            petCell = '<td> </td>'
        else:
            pett = time.strptime(rpet_str[0:19],"%Y-%m-%dT%H:%M:%S")
            petCell = '<td> ' + time.asctime(pett) + '</td>'
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
        
        if spot['paid'] == 1:
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

