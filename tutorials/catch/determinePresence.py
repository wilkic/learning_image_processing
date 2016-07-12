
import numpy as np

####
def determinePresence( spot ):
    
    m = np.asarray(spot['means'])
    b = np.asarray(spot['base_means'])

    dMean = m - b

    meanPresence = np.where( dMean > spot['meanThresh'] )
    spot['mPresent'] = len( meanPresence ) > 1

    spot['kPresent'] = spot['nKeys'] > spot['keyThresh']

    spot['ePresent'] = spot['nEdges'] > spot['edgeThresh']
    
    # Give out the final score
    present = spot['ePresent']
    
    return present


