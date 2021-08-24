# Sketches of routines to add to MoDX API
#
# Author: Ben Krepp 
# Date:   23 August 2021

import csv
import numpy as np
import pandas as pd
import geopands as gp
from dbfread import DBF
import pydash

_version = 0.0.1
def get_version():
    return _version
#

# Internal variables, pseudo-constants, etc.
#
_all_time_periods = ['am', 'md', 'pm', 'nt']
_auto_modes = [ 'SOV', 'HOV' ]
_truck_modes = [ 'Heavy_Truck', 'Heavy_Truck_HazMat', 'Medium_Truck', 'Medium_Truck_HazMat', 'Light_Truck' ]
_nm_modes = [ 'Walk', 'Bike' ]
_transit_modes = [ 'DAT_Boat', 'DET_Boat', 'DAT_CR', 'DET_CR', 'DAT_LB', 'DET_LB', 'DAT_RT', 'DET_RT', 'WAT' ]
_all_modes = _auto_modes + _truck_modes + _nm_modes + _transit_modes

#
# Section 1: Trip table management
#
# Function: load_tts_as_np_arrays
#
# Summary: Load the trip tables for the specified list of time periods for the specified list of modes as NumPy arrays.
#          If no list of time periods is passed, trip tables for all time periods will be returned.
#          If no list of modes is passed, trip tables for all modes will be returned.
#
# Parameters:   tts             - trip tables, a dict (keys: 'am', 'md', 'pm', and 'nt'),
#                                 each element of which is an '.omx' trip table file that has 
#                                 been opened using the openmatrix library
#               time_periods    - list of time periods (strings), or None
#               mode_list       - list of modes (strings), or None
#
# Return value: A two-level dictionary (i.e., first level = time period, second level = mode)
#               the second level of which contain the trip table, in the form of a numPy array,
#               for the [time_period][mode] in question.
#
def load_tts_as_np_arrays(tts, time_periods=None, mode_list=None):
    if time_periods == None:
        time_periods = _all_time_periods
    #
    if mode_list == None:
        mode_list = _all_modes
    #
    retval = {}
    for period in time_periods:
        retval[period] = None
    #
    for period in time_periods:
        retval[period] = {}
        for mode in mode_list:
            temp = tts[period][mode]
            retval[period][mode] = np.array(temp)
        # end_for
    # end_for
    return retval
# end_def load_tts_for_mode_list_as_np_arrays()

#
# Section 2: TAZ "shapefile" management
#
# Summary: The class "tazManager" provides a set of methods to perform _attribute_ queries
#          on an ESRI-format "Shapefile" that represents the TAZes in the model region.
#          The attributes are read from the Shapefile's .DBF file; other components of
#          the Shapefile are ignored.
#
#          The Shapefile's .DBF file _must_ contain the following attributes:
#              1. id
#              2. taz
#              3. type - 'I' (internal) or 'E' (external)
#              4. town
#              5. state - state abbreviation, e.g., 'MA'
#              6. town_state - town, state
#              7. mpo - abbreviation of MPO name: 
#              8 in_brmpo - 1 (yes) or 0 (no)
#              9. subregion - abbreviation of Boston Region MPO subregion or NULL
#
#         An objectd of class tazManager is instantiated by passing in the fully-qualified path
#         to a Shapefile to the class constructor. Hence, it is possible to have more than one
#         instance of this class active simultaneously, should this be needed.
#
# Class tazManager
# Methods:
#   1. __init__(path_to_shapefile) - class constructor
#   2. mpo_to_tazes(mpo) - Given the name (i.e., abbreviation) of an MPO,
#      return a list of the records for the TAZes in it
#   3. brmpo_tazes() - Return the list of the records for the TAZes in the Boston Region MPO
#   4. brmpo_town_to_tazes(town) - Given the name of a town in the Boston Region MPO,
#      return a list of the records for the TAZes in it
#   5. brmpo_subregion_to_tazes(subregion) - Given the name (i.e., abbreviation) of a Boston Region MPO subregion,
#      return a list of the records for the TAZes in it
#   6. town_to_tazes(town) - Given the name of a town, return the list of the records for the TAZes in the town.
#      Note: If a town with the same name occurs in more than one state, the  list of TAZes
#      in _all_ such states is returned.
#   7. town_state_to_tazes(town, state) - Given a town and a state abbreviation (e.g., 'MA'),
#      return the list of records for the TAZes in the town
#   8. state_to_tazes(state) - Given a state abbreviation, return the list of records for the TAZes in the state.
#   9. taz_ids(TAZ_record_list) - Given a list of TAZ records, return a list of _only_ the TAZ IDs from those records.
#
# Note:
# For all of the above API calls that return a "list of TAZ records", each returned 'TAZ' is a Python 'dict' containing
#  all of the keys (i.e., 'attributes') listed above. To convert such a list to a list of _only_ the TAZ IDs, call taz_ids
# on the list of TAZ records.
#

class tazManager():
    _instance = None
    _default_base = r'C:/Users/ben_k/work_stuff/modx_data/canonical_TAZ_shapefile/'
    _default_shapefile_fn = 'candidate_CTPS_TAZ_STATEWIDE_2019.shp'
    _default_fq_shapefile_fn = _default_base + _default_shapefile_fn
    _taz_table = []
    
    def __init__(self, my_shapefile_fn=None):
        # print('Creating the tazManager object.')
        if my_shapefile_fn == None:
            my_shapefile_fn = _default_fq_shapefile_fn
        #
        # Derive name of .dbf file 
        my_dbffile_fn = my_shapefile_fn.replace('.shp', '.dbf')
        dbf_table = DBF(my_dbffile_fn, load=True)
        for record in dbf_table.records:
            new = {}
            new['id'] = int(record['id'])
            new['taz'] = int(record['taz'])
            new['type'] = record['type']
            new['town'] = record['town']
            new['state'] = record['state']
            new['town_state'] = record['town_state']
            new['mpo'] = record['mpo']
            new['in_brmpo'] = int(record['in_brmpo'])
            new['subregion'] = record['subregion']
            self._taz_table.append(new)
        # end_for
        dbf_table.unload()
        print('Number of recrods read = ' + str(len(self._taz_table)))
        return self._instance
    # end_def __init__()
    
    # For debugging during development:
    def _get_tt_item(self, index):
        return self._taz_table[index]
        
    def mpo_to_tazes(self, mpo):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['mpo'] == mpo)
        return retval

    def brmpo_tazes(self):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['in_brmpo'] == 1)
        return retval

    def brmpo_town_to_tazes(self, mpo_town):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['in_brmpo'] == 1 and x['town'] == mpo_town)
        return retval

    def brmpo_subregion_to_tazes(self, mpo_subregion):
        # We have to be careful as some towns are in two subregions,
        # and for these the 'subregion' field of the table contains
        # an entry of the form 'SUBREGION_1/SUBREGION_2'.
        retval = []
        if subregion == 'ICC':
            retval = pydash.collections.filter_(self._taz_table, 
                                                lambda x: x['subregion'].find('ICC') != -1)
        elif subregion == 'TRIC':
            retval = pydash.collections.filter_(self._taz_table, 
                                                lambda x: x['subregion'].find('TRIC') != -1)
        elif subregion == 'SWAP':
            retval = pydash.collections.filter_(self.taz_table,
                                                lambda x: x['subregion'].find('SWAP') != -1)
        else:
            retval = pydash.collections.filter_(self._taz_table, lambda x: x['subregion'] == mpo_subregion)
        # end_if
        return retval
    # def_def mpo_subregion_to_tazes()
    
    # Note: Returns TAZes in town _regardless_ of state.
    def town_to_tazes(self, town):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['town'] == town)
        return retval

    def town_state_to_tazes(self, town, state):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['state'] == state and x['town'] == town)
        return retval

    def state_to_tazes(self, state):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['state'] == state)
        return retval
        
    def taz_ids(self, taz_record_list):
        retval = []
        for taz in taz_record_list:
            retval.append(taz['id'])
        # end_for
        return retval
# end_class tazManager

#
# Section 3: Dataframe and Geo-dataframe utilities
#

# Export specified list of columns of a dataframe to a CSV file.
# If a list of columns isn't specified, export all columns.
def export_df_to_csv(dataframe, csv_fn, column_list=None):
	if column_list != None:
		dataframe.to_csv(csv_fn, sep=',', column_list)
	else:
		dataframe.to_csv(csv_fn, sep=',')
# end_def
# 

# Export a geo-dataframe to a GeoJSON file.
def export_gdf_to_geojson(geo_dataframe, geojson_fn):
        geo_dataframe.to_file(geojson_fn, driver='GeoJSON')
#
        
# Export a geo-dataframe to an ESRI-format shapefile.
# Note: Attribute (property) names longer than 10 characters will be truncated,
#       due to the limitations of the DBF file used for Shapefile attributes.
def export_gdf_to_shapefile(geo_dataframe, shapefile_fn):
        geo_dataframe.to_file(shapefile_fn, driver='ESRI Shapefile')
#

