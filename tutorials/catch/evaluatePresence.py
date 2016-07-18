

import time

####
def evaluatePresence( spot, present, delta_time, ts ):
    
    # If car is present, mark as taken
    # otherwise reset counter
    leaving = 0
    if present:
        spot['timePresent'] += delta_time
    else:
        if spot['timePresent'] >= spot['occupationThresh']:
            leaving = 1
        spot['timePresent'] = 0
    
    # if wasn't occupied, occupance will be new
    new_occupation = spot['timeOccupied'] == 0
    
    # Mark as occupied once spot has been taken for time past threshold
    occupied = spot['timePresent'] >= spot['occupationThresh']
    
    # By default don't send a message
    message = None

    # When spot is flagged as occupied, notify 
    ts_gmt = time.gmtime(ts)
    ts_str = time.asctime(ts_gmt)
    if occupied and new_occupation:
        
        spot['occupationStartTime'] = ts
        
        message = """
        Spot %d taken at %s!
        """ % ( spot['number'], ts_str )
        print message
    
    # Record duration of occuption
    spot['timeOccupied'] = 0
    if occupied:
        spot['timeOccupied'] = ts - spot['occupationStartTime']
        
    # When spot is vacated, notify too
    if leaving:
        
        spot['occupationEndTime'] = ts
        
        message = """
        %s
        Car left spot %d at %s!
        %s """ % ( spot['number'], ts_str )
        print message

    return message

