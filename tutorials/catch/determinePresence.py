
import numpy as np

####
def determinePresence( spot ):
    
    m = np.asarray(spot['means'])
    b = np.asarray(spot['base_means'])

    dMean = abs(m - b)

    meanPresence = np.where( dMean > spot['meanThresh'] )
    spot['mPresent'] = len( meanPresence ) > 0
    
    dKeys = spot['nKeys'] - spot['base_nKeys']
    spot['kPresent'] = dKeys > spot['keyThresh']

    dEdges = spot['nEdges'] - spot['base_nEdges']
    spot['ePresent'] = dEdges > spot['edgeThresh']
    
    # All criteria must be met
    present = True
    for s in spot['detectionType']:
        pstr = s + 'Present'
        present = present and spot[pstr]
    
    return present


