# First crack at more meaningful route classification for transit report.
#
# Define data structure and function classify transit routes for reporting purposes.
_classification_table = {
    1:  'MBTA Local Bus',
    2:  'MBTA Express Bus',
    3:  'MBTA Express Bus' ,
    4:  'Green Line',
    5:  'Red Line',
    6:  'Mattapan Trolley',
    7:  'Orange Line',
    8:  'Blue Line',
    9:  'Commuter Rail',
    10: 'Inner Harbor Ferry',
    11: 'Other Ferries',
    12: 'Silver Line',
    13: 'Sliver Line',
    14: 'Logan Express',
    15: 'Logan Shuttle',
    16: 'MGH and Other Shuttles',
    17: 'Brockton RTA Bus',
    18: 'CATA Bus',
    19: 'GATRA Bus',
    20: 'Lowell RTA Bus',
    21: 'Merrimack RTA Bus',
    22: 'MetroWest RTA Bus',
    23: 'Bloom Bus (private)',
    24: 'C & J Bus (private)',
    25: 'Boston Express Bus (private)',
    26: 'Concord Coach Bus (private)',
    27: 'Dattco Bus (private)',
    28: 'Plymouth & Brockton Bus (private)',
    29: 'Peter Pan Bus (private)',
    30: 'Yankee Bus (private)',
    31: 'Miscellaneous Bus Routes',
    32: 'Commuter Rail',
    33: 'Commuter Rail',
    34: 'Commuter Rail',
    35: 'Commuter Rail',
    36: 'Commuter Rail',
    37: 'Commuter Rail',
    38: 'Commuter Rail',
    39: 'Commuter Rail',
    40: 'Commuter Rail',
    41: 'SRTA Bus',
    42: 'Worcester RTA Bus',
    43: 'PVTA RTA Bus',
    44: 'Unknown RTA Bus',
    70: 'Walk' }

def classify_green_line_route(row):
    # Crude, first-crack implementation based on TDM19 'Routes_ID' field.
    retval = 'Green Line - '
    route_id = row['Routes_ID']
    if route_id in [6034, 6035]:
        retval += 'B'
    elif route_id in [6032, 6033]:
        retval += 'C'
    elif route_id in [6036, 6037]:
        retval += 'D'
    elif route_id in [8393, 8394]:
        retval += 'E'
    elif route_id in [6038, 6039]:
        retval += 'D (GLX)'
    elif route_id in [6028, 6029]:
        retval += 'E (GLX)'
    else:
        retval += 'UNKNONWN'
    # end_if 
    return retval
    
def classify_silver_line_route(row):
    # Crude, first-crack implementation based on Ed Bromage's 'Mode'
    # and the TDM19 'Routes_ID' field.
    retval = 'Silver Line - '
    ed_mode = row['Mode']
    if ed_mode == 13:
        retval += 'Washington Street'
    else:
        # ed_mode == 12
        route_id = row['Routes_ID']
        if route_id in [6050, 6051]:
            retval += 'Drydock'
        elif route_id in [6055, 6056]:
            retval += 'Logan Airport'
        elif route_id in [6058, 6059, 8256, 8257, 8258, 8259, 8260, 8261]:
            retval += 'Chelsea'
        else:
            retval += 'UNKNOWN'
        # end_if
    # end_if  
    return retval
    
def classify_commuter_rail_route(row):
    # Crude, first-crack implementation based on solely Ed Bromage's 'Mode'.
    # This implementation could be moved into the calling logic, but is
    # placed here in expectation that further refinement will be needed.
    # Yes, this version could have been implemented with a lookup table...
    ed_mode = str(row['Mode'])
    retval = 'Commuter Rail - '
    if ed_mode == 9:
        retval += 'Fairmount Line'
    elif ed_mode == 32:
        retval += 'Beverly / Newburyport / Rockport Line'
    elif ed_mode == 33:
        retval +=  'Stoughton / Providence Line'
    elif ed_mode == 34:
        retval +=  'Kingston Line'
    elif ed_mode == 35:
        retval += 'Haverhill Line'
    elif ed_mode == 36:
        retval = temp + 'Lowell Line'
    elif ed_mode == 37:
        retval += 'Fitchburg Line'
    elif ed_mode == 38:
        retval += 'Framingham / Worcester Line'
    elif ed_mode == 39:
        retval += 'Needham Line'
    elif ed_mode == 40:
        retval += 'Franklin Line'
    else:
        retval += 'UNKNOWN'
    # end_if
    return retval
# end_def classify_commuter_rail_route()

def classify_transit_route(row):
    retval = 'None'
    eds_mode = row['Mode']
    if eds_mode == 4:
        retval = classify_green_line_route(row)
    elif eds_mode in [12, 13]:
        retval = classify_silver_line_route(row)
    elif eds_mode in [9,34, 35, 36, 37, 38, 39, 40]:
        retval = classify_commuter_rail_route(row)
    elif eds_mode in _classification_table:
        retval = _classification_table[eds_mode]
    # end_if
    return retval
# end_def classify_transit_route()
