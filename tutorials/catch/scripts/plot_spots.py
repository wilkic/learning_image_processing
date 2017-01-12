

import csv
import os, sys
import re
sys.path.append('..')
import loadCameras as lc

def get_spot_data(log_dir,plot_spots=None):
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
        
        if not plot_spots is None:
            if sn not in plot_spots:
                continue

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

plot_spots = range(1,38+1) + range(43,49+1)
tmin = -24
tmax = 0

fdir = os.path.expanduser('~/work/aws/spot_logs')
spots = get_spot_data(fdir,plot_spots)
cams = lc.loadCameras()

for c,cam in cams.iteritems():
    for s in cam['spots']:
        if s['number'] not in plot_spots:
            continue
        si = next(i for i in spots if i['num'] == s['number'])
        si['klim'] = s['keyThresh'] + s['base_nKeys']
        si['elim'] = s['edgeThresh'] + s['base_nEdges']
        si['mhlim'] = [0,0,0]
        si['mllim'] = [0,0,0]
        for i in range(3):
            si['mhlim'][i] = s['base_means'][i] + s['meanThresh']
            si['mllim'][i] = s['base_means'][i] - s['meanThresh']

    
c = ['r','g','b']


#plt.ion()
#plt.figure()

i = 1
for s in spots:
   
    if 'plot_spots' in locals():
        if s['num'] not in plot_spots:
            continue

    time = np.asarray(s['ts'])
    t2end = (time - time[-1]) / 3600
    
    inds = np.where( np.bitwise_and( t2end > tmin, t2end < tmax ) )

    keylim = s['klim']
    edgelim = s['elim']
    mhlim = s['mhlim']
    mllim = s['mllim']
    nks = np.asarray( s['nKeys'] )
    nes = np.asarray( s['nEdges'] )
    
    
    dname = 'pics'
    if not os.path.exists(dname):
        os.makedirs(dname)


    #plt.subplot( 3,1,i)
    plt.figure()
    plt.plot( t2end[inds], nks[inds] )
    plt.plot( t2end[inds], keylim*np.ones_like(t2end[inds]) )
    plt.title( 'Spot %d: nKeys' % s['num'] )

#    for i in range(3):
#        plt.plot(s['ts'],s['means'][i],c[i])
    
    #plt.show()
    fname = 'spot' + str(s['num']) + '_nkeys.png'
    fname = os.path.join(dname,fname)
    plt.savefig(fname)

    plt.close()
    #plt.waitforbuttonpress(timeout=-1)
    
    
    
    plt.figure()
    plt.title( 'Spot %d: means' % s['num'] )
    for i in range(3):
        m = np.asarray( s['means'][i] )
        plt.plot(t2end[inds],m[inds],c[i])
        plt.plot(t2end[inds], mhlim[i]*np.ones_like(t2end[inds]) )
        plt.plot(t2end[inds], mllim[i]*np.ones_like(t2end[inds]) )
    
    #plt.show()
    fname = 'spot' + str(s['num']) + '_means.png'
    fname = os.path.join(dname,fname)
    plt.savefig(fname)

    plt.close()
    #plt.waitforbuttonpress(timeout=-1)
    

    
    
    plt.figure()
    plt.plot( t2end[inds], nes[inds] )
    plt.plot( t2end[inds], edgelim*np.ones_like(t2end[inds]) )
    plt.title( 'Spot %d: nEdges' % s['num'] )

    #plt.show()
    fname = 'spot' + str(s['num']) + '_nedges.png'
    fname = os.path.join(dname,fname)
    plt.savefig(fname)

    plt.close()
    #plt.waitforbuttonpress(timeout=-1)

    i += 1

plt.figure()
plt.close()

sort_spots = sorted( spots, key=lambda k: k['num'] )

html = """
<html>
    <head>
    <title>Spot Plots</title>
    </head>
    <body>"""
for s in sort_spots:
    ss = str(s['num'])
    
    html += '<h2>'
    html += 'Spot ' + ss + ' History'
    html += '</h2>'
    
    fname = dname + '/spot' + ss + '_nkeys.png'
    html += '<img src="' + fname + '" style="width:304px;height:228px;">'

    fname = dname + '/spot' + ss + '_means.png'
    html += '<img src="' + fname + '" style="width:304px;height:228px;">'
    
    fname = dname + '/spot' + ss + '_nedges.png'
    html += '<img src="' + fname + '" style="width:304px;height:228px;">'


html += '</body></html>'

with open('index.html','w') as f:
    f.write(html)

