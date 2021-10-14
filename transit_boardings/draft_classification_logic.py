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
    14: 'Logan Express,
    15: 'Logan Shuttle',
    16: 'MGH and Other Shuttles',
    17: 'Brockton RTA Bus',
    18: 'CATA Bus',
    19: 'GATRA Bus',
    20: 'Lowell RTA Bus',
    21: 'Merrimack RTA Bus',
    22: 'MetroWest RTA Bus',
    23: 'Boom Bus (private)',
    24: 'C & J Bus (private)',
    25: 'Boston Express Bus (private)',
    26: 'Coach Co Bus (private)',
    27: 'Dattco Bus (private)',
    28: 'Plymouth & Brockton Bus (private)',
    29: 'Peter Pan Bus (private)',
    30: 'Yankee Concord Bus (private)',
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
	retval = '???'
	return retval
	
def classify_silver_line_route(row):
	retval = '??????'
	return retval
	
def classify_commuter_rail_route(row):
	retval = '?????????'
	return retval

def classify_transit_route(row):
    retval = 'None'
	eds_mode = row['Mode']
	if eds_mode == 4:
		retval = classifiy_green_line_route(row)
	elif eds_mode in [12, 13]:
		retval = classify_silver_line_route(row)
	elif eds_mode in [9,34, 35, 36, 37, 38, 39, 40]:
		retval = classify_commuter_rail_route(row)
    elif eds_mode in _classification_table:
        retval = _classification_table[mode]
    # end_if
	return retval
# end_def classify_transit_route()
