
import numpy as np
import sys

####
def determinePresence( spot ):
    
    m = np.asarray(spot['means'])
    b = np.asarray(spot['base_means'])

    dMean = abs(m - b)

    meanPresence = np.where( dMean > spot['meanThresh'] )
    spot['mPresent'] = len( meanPresence[0] ) > 0
    
    dKeys = spot['nKeys'] - spot['base_nKeys']
    spot['kPresent'] = dKeys > spot['keyThresh']

    dEdges = spot['nEdges'] - spot['base_nEdges']
    spot['ePresent'] = dEdges > spot['edgeThresh']
    
    # Can have more than one criteria

    # Check the first one
    present = True
    sdt = spot['detectionType']
    dt = sdt[0]
    pstr = dt + 'Present'
    present = present and spot[pstr]
    
    # Check remaining ones if there
    l = len(sdt)
    if l > 1:
        detection_types = ['m','k','e']
        expr_types = ['&','|']

        expr = 'present=present'
        no_operator_specified = True
        
        for dt in sdt[1:]:
            if dt in detection_types:
                if no_operator_specified:
                    expr += '&'
                else:
                    no_operator_specified = True
                pstr = dt + 'Present'
                expr = expr + "spot['" + pstr + "']"

            elif dt in expr_types:
                expr += dt
                no_operator_specified = False

            else:
                msg = "Unknown type: %s" % dt
                print msg
                sys.exit()

        exec(expr)

    
    return present


