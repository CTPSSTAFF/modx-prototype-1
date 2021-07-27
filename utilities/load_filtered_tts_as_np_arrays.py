# Function: load_filtered_tts_as_np_arrays
#
# Summary load all trip tables (i.e, for all time periods, for all modes) as NumPy arrays,
# filter these NumPy arrays using the filter_arr parameter,
# and return a two-level dictionary (i.e., by time period and by mode) of the results.
#
period_list = ['am', 'md', 'pm', 'nt']
mode_list = ['SOV', 'HOV', 'Heavy_Truck', 'Heavy_Truck_HazMat', 'Medium_Truck', 'Medium_Truck_HazMat', 'Light_Truck',
             'Walk', 'Bike', 'DAT_Boat', 'DET_Boat', 'DAT_CR', 'DET_CR', 'DAT_LB', 'DET_LB', 'DAT_RT', 'DET_RT', 'WAT' ]
#
def load_filtered_tts_as_np_arrays(tts, filter_arr):
    retval = {'am' : None, 'md' : None, 'pm' : None, 'nt' : None }
    for period in period_list:
        print(period)
        retval[period] = {}
        for mode in mode_list:
            print(mode)
            temp1 = tts[period][mode]
            temp2 = np.array(temp1)
            retval[period][mode] = temp2[filter_arr]
        # end_for
    # end_for
    return retval
# end_def
