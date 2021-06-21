# Miscellanea collected in the course of working on this prototype.
# This material may or may not have value in the long-term, but is being captured here just in case it might.
#
# -- B. Krepp 21 June 2021

# Function: csv_to_np_array(csv_fn)
# 
# Summary: Given the full pathname to a CSV file,
#                read the CSV file, extracting the column headers,
#                and converting the data in the remaining rows into
#                a numpy array.
#
# Assumption: The "cells" of the CSV file have uniform floating-point data type
#
# Return value: Python 'dict' containing:
#     column_names - Python list of column names
#     np_array - numpy array of values in the CSV file, excluding the column headers
#
def csv_to_np_array(csv_fn):
    temp_list = []
    with open(csv_fn, newline='') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        for row in myreader:
            temp_list.append(row)
    #
    # Save the column names in a separate list, and remove them from 'temp_list'
    column_names = temp_list[0]
    temp_list.pop(0)

    # Convert all the data in temp_list (which is of string type) to floating point type, 
    # so it can be loaded into a numpy array.
    # We accumulate the converted data in a "parallel" list/array, retval_list.
    #
    retval_list = []
    for r in temp_list:
        new_row = []
        for c in r:
            # *** WARNING: HACK! to work around cells with no data.
            temp = float(c) if c != '' else 0.0
            new_row.append(temp)
        #
        retval_list.append(new_row)
    #

    # Load retval_list into a numpy array, the function's return value.
    np_array = np.array(retval_list)
    #
    # Function return value is a dict consisting of:
    #     column_names - Python list of column names
    #     np_array - numpy array of values in the CSV file, excluding the column headers
    #
    retval = { 'column_names' : column_names, 'np_array' : np_array }
    return retval
# end_def csv_to_np_array
