# Given a dict called "taz_to_omxid" that maps TAZ ID to OMX ID, create dict to map OMX ID to TAZ ID:
#
taz_to_omxid_keys = taz_to_omxid.keys()
taz_to_omxid_values = taz_to_omxid.values()
omxid_to_taz = dict(zip(taz_to_omxid_values, taz_to_omxid_keys))
