

import time

####
def evaluatePresence( spot ):
    
    # If car is present, mark as taken
    # otherwise reset counter
    leaving = 0
    if present > 1:
        spot['time_present'] += delta_time
    else:
        if spot['time_present'] >= spot['persistence_threshold']:
            leaving = 1
        spot['time_present'] = 0
    
    # if wasn't occupied, occupance will be new
    new_occupation = not spot['occupied']
    
    # Mark as occupied once spot has been taken for time past threshold
    spot['occupied'] = spot['time_present'] >= spot['persistence_threshold']
    
    # By default don't send a message
    message = None

    # When spot is flagged as occupied, notify 
    ts_gmt = time.gmtime(camera['im_ts'])
    ts_str = time.asctime(ts_gmt)
    if spot['occupied'] and new_occupation:
        
        spot['occupationStartTime'] = ts_str
        
        message = """
        Spot %d taken at %s!
        """ % ( spot['number'], ts_str )

    # When spot is vacated, notify too
    if leaving:
        
        spot['occupationEndTime'] = ts_str
        
        message = """
        %s
        Car left spot %d at %s!
        %s """ % ( spot['number'], ts_str )

    return message

