

import csv
import os, sys
import re
sys.path.append('..')
import loadCameras as lc

def get_spot_data(log_dir):
    spots = []

    f = []
    for (dirpath, dirnames, filenames) in os.walk(log_dir):
        f.extend(filenames)
        break

    for s in f:
        #fname = 'spot' + str(s) + '.log'
        #ffname = os.path.join(log_dir,fname)
        ffname = os.path.join(log_dir,s)
        ft = os.path.splitext(s)
        sn = int( ft[0][4:] )
        ts = []
        tp = []
        means = [[], [], []]
        sigs = [[], [], []]
        maxs = [[], [], []]
        mins = [[], [], []]
        nEdges = []
        nKeys = []
        with open(ffname) as f:
            rdr = csv.reader(f)
            for r in rdr:
                ts += [float(r[0])]
                tp += [float(r[1])]
                for i in range(3):
                    means[i] += [float(r[2+i])]
                    sigs[i] += [float(r[5+i])]
                    maxs[i] += [float(r[8+i])]
                    mins[i] += [float(r[11+i])]
                nEdges += [float(r[14])]
                nKeys += [float(r[15])]

        spot = {
            'num':sn,
            'ts':ts,
            'tp':tp,
            'means':means,
            'sigs':sigs,
            'maxs':maxs,
            'mins':mins,
            'nEdges':nEdges,
            'nKeys':nKeys,
            'klim':0
        }

        spots += [spot]

    return spots


#######################################
#######################################
#######################################

import matplotlib.pyplot as plt
import numpy as np

fdir = os.path.expanduser('~/work/aws/spot_logs')
spots = get_spot_data(fdir)
cams = lc.loadCameras()

for c,cam in cams.iteritems():
    for s in cam['spots']:
        si = next(i for i in spots if i['num'] == s['number'])
        si['klim'] = s['keyThresh'] + s['base_nKeys']

    
c = ['r','g','b']

#plots_spots = [9, 10]

for s in spots:
    
#    if s['num'] not in plots_spots:
#        continue

    time = np.asarray(s['ts'])
    t2end = (time - time[-1]) / 60

    keylim = s['klim']
    plt.ion()
    plt.figure()
    plt.plot( t2end, s['nKeys'] )
    plt.plot( t2end, keylim*np.ones_like(t2end) )

#    for i in range(3):
#        plt.plot(s['ts'],s['means'][i],c[i])
    
    #plt.show()
    fname = 'spot' + str(s['num']) + '.png'
    plt.savefig(fname)

plt.figure()
plt.close()

sort_spots = sorted( spots, key=lambda k: k['num'] )

html = '<html><body>'
for s in sort_spots:
    ss = str(s['num'])
    fname = 'spot' + ss + '.png'
    html += '<h2>'
    html += 'Spot ' + ss + ' History'
    html += '</h2>'
    html += '<img src="' + fname + '" style="width:304px;height:228px;">'

html += '</body></html>'

with open('index.html','w') as f:
    f.write(html)

