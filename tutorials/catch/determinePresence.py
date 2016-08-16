
import numpy as np

####
def determinePresence( spot ):
    
    m = np.asarray(spot['means'])
    b = np.asarray(spot['base_means'])

    dMean = m - b

    meanPresence = np.where( dMean > spot['meanThresh'] )
    spot['mPresent'] = len( meanPresence ) > 1
    
    dKeys = spot['nKeys'] - spot['base_nKeys']
    spot['kPresent'] = dKeys > spot['keyThresh']

    dEdges = spot['nEdges'] - spot['base_nEdges']
    spot['ePresent'] = dEdges > spot['edgeThresh']
    
    # Give out the final score
    if spot['detectionType'] == 'ke':
        present = spot['ePresent'] and spot['kPresent']
    else:
        # Do key detection alone in general
        present = spot['kPresent']
    
    return present


