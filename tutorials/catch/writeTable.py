
import ipdb

import os, sys
import time

sys.path.append(os.getcwd())

import html_ops as ho

def writeTable( spots ):

    # Put the data in a table
    tabHtml = '<div id="latable">'
    tabHtml += '<input class="search" placeholder="Search" />'
    tabHtml += """
    <button class="sort" data-sort="timp">
      Sort by Time Present
    </button>
    <button class="sort" data-sort="pd">
      Sort by Paid
    </button>
    <table border="1">"""

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

    tabHtml += '<tbody class="list">'

    n_remaining = len(spots)

    for spot in spots:

        # For now, update remaining number of
        # spots based on the number paid
        n_remaining -= spots[spot]['paid']

        row = '<tr>'
        spaceCell = '<td>Space ' + str(spot) + '</td>'
        occCell = '<td> ' + str(spots[spot]['timeOccupied']>0) + '</td>'
        presCell = ( '<td class="timp"> '
                     + str(spots[spot]['timePresent'])
                     + '</td>' )
        paidCell = ( '<td class="pd"> '
                     + str(spots[spot]['paid'])
                     + '</td>' )
        rpst_str = str(spots[spot]['payStartTime'])
        rpet_str = str(spots[spot]['payEndTime'])
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
        lpnCell = '<td> ' + str(spots[spot]['lpn']) + '</td>'
        lpsCell = '<td> ' + str(spots[spot]['lps']) + '</td>'
        mnthCell = '<td> ' + str(spots[spot]['monthly']) + '</td>'
        ost_lt = time.localtime(spots[spot]['occupationStartTime'])
        oet_lt = time.localtime(spots[spot]['occupationEndTime'])
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
    
    tabHtml += '</tbody>'
    tabHtml += '</table>'
    tabHtml += '</div>'
    tabHtml += """
    <script src="http://listjs.com/no-cdn/list.js"></script>
    <script>
      var options = {
       valueNames: [ 'pd', 'timp' ]
      };

      var userList = new List('latable', options);
    </script>"""

    ho.write_page( 'table.html', 'Lot Status', 30, tabHtml )
    #os.rename("table.html","/var/www/html/table/index.html")
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

