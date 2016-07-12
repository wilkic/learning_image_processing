
def createSpots()

    # Set up the spots dictionary
    nSpots = 49

    # These spots are monthly
    monthlies = [39, 40, 41, 42]

    defaultProperties = {
        'paid': 0,
        'payStartTime': '',
        'payEndTime': '',
        'lps': '',
        'lpn': '',
        'monthly': 0,
        'occupied': 0,
        'present': 0,
        'occupationStartTime': 0,
        'occupationEndTime': 0
    }

    spots = {prop:defaultProperties.copy() for prop in range(1,nSpots+1)}

    # Assign the monthlies
    for i in monthlies:
        spots[i]['monthly'] = 1
        spots[i]['paid'] = 1

    return spots

