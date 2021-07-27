# Generate a filter array to be used to remove all but the external TAZes from each of the trip tables.
#
# Method:
#    1. Get a list of the OMX IDs of the 'external' TAZes
#    2. Create an array of boolean values, indexed by OMXID, where the value of each element indicates whether 
#       the corresponding is or is not that of an 'external' TAZ. (This array is known as a 'filter_array'.)
#
# Generate filter array, Step 1 : Get a list of the OMX IDs of the 'external' TAZes.
#
# Given the "taz_to_omxid" dict that maps TAZ ID to OMX ID, create dict to map OMX ID to TAZ ID:
#
taz_to_omxid_keys = taz_to_omxid.keys()
taz_to_omxid_values = taz_to_omxid.values()
omxid_to_taz = dict(zip(taz_to_omxid_values, taz_to_omxid_keys))
# Generate filter array, Step 2 - Actually create the filter array.
#
first_external_taz = 209001
filter_list = []
keys = omxid_to_taz.keys()
for k in keys:
    if omxid_to_taz[k] > first_external_taz:
        filter_list.append(True)
    else:
        filter_list.append(False)
    # end_if
# end_for
