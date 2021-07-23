#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Total external trips notebook

import openmatrix as omx
import numpy as np
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
import bokeh
import xarray as xr
import hvplot.pandas
import hvplot.xarray


# In[2]:


# Root directory for MoDX output for "base year" model results.
#
base_scenario_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2016 Scen 00_08March2019_MoDXoutputs/'
#
# Root directory for MoDX output for "comparison scenario" model results.
# 
comparison_scenario_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2040 NB Scen 01_MoDXoutputs/'


# In[3]:


# ===>>>USER INPUT REQUIRED: <<<===
#
# Supply path to root directory of scenario to use for the current run of this notebook:
# 
home_dir = base_scenario_dir


# In[4]:


taz_shapefile_base_dir = r'G:/Data_Resources/modx/canonical_TAZ_shapefile/'


# In[5]:


# trip_tables directory - this really "should" be a subdirectory of the base directory, but is isn't currently.
# The real McCoy - where things should go, and will eventually go
tt_dir = home_dir + 'out/'


# In[6]:


# trip tables OMX file (matrices)
tt_am = tt_dir + 'AfterSC_Final_AM_Tables.omx'
tt_md = tt_dir + 'AfterSC_Final_MD_Tables.omx'
tt_pm = tt_dir + 'AfterSC_Final_PM_Tables.omx'
tt_nt = tt_dir + 'AfterSC_Final_NT_Tables.omx'
trip_tables = { 'am' :  omx.open_file(tt_am, 'r'),
                'md' : omx.open_file(tt_pm, 'r'),
                'pm' : omx.open_file(tt_pm,'r'),
                'nt'  : omx.open_file(tt_nt, 'r') }


# In[7]:


num_tazes = trip_tables['am'].shape()[0]


# In[8]:


# Mapping from TAZ-ID to OMX index for the 4 periods (these *should* be the same)
taz_to_omxid_am = trip_tables['am'].mapping('ID')
taz_to_omxid_am = trip_tables['md'].mapping('ID')
taz_to_omxid_pm = trip_tables['pm'].mapping('ID')
taz_to_omxid_nt =  trip_tables['nt'].mapping('ID')


# In[9]:


# We'll assume that the mapping from TAZ ID to OMX ID doesn't vary by time period.
# We'll use the AM mapping as _the_ mapping for all time periods, pending confirmation.
# 
# TBD: Insert "sanity check" that the 4 mappings on "ID" are identical.
#
taz_to_omxid = taz_to_omxid_am


# In[10]:


# Function: tt_total_for_mode
#
# Summary: Return the total travel demand, over all i and j, from TAZ[i] to TAZ[j] for the specified mode.
#
# Given the OMX trip tables for the 4 time periods and a mode,
# return an numpy array with the "numpy sum" of the data in the OMX array for the 4 time periods.
def tt_total_for_mode(tts, mode):
	am = tts['am'][mode]
	md = tts['md'][mode]
	pm = tts['pm'][mode]
	nt =  tts['nt'][mode]
	# Convert OMX arrays into numpy arrays
	am_np = np.array(am)
	md_np = np.array(md)
	pm_np = np.array(pm)
	nt_np = np.array(nt)
	total = am_np + md_np + pm_np + nt_np
	return total
# end_def tt_total_for_mode


# In[11]:


# Function to generate the calculation to total demand for a list of modes.
# Return a dictionary containing the total demand for each mode, with the key value == the mode name
def tt_totals_for_mode_list(tts, mode_list):
    retval = {}
    for mode in mode_list:
        temp = tt_total_for_mode(tts, mode)
        retval[mode] = temp
    #
    return retval
# end_def tt_total_for_mode_list


# In[12]:


# *** Careful about running this ... it is a large hammer!
# It would be better to have factored out all but the external TAZes from the trip_tables to begin with...
# Haven't yet figured out a good/clean way to do that...
#
mode_list = ['SOV', 'HOV', 'Heavy_Truck', 'Heavy_Truck_HazMat', 'Medium_Truck', 'Medium_Truck_HazMat', 'Light_Truck',
             'Walk', 'Bike', 'DAT_Boat', 'DET_Boat', 'DAT_CR', 'DET_CR', 'DAT_LB', 'DET_LB', 'DAT_RT', 'DET_RT', 'WAT' ]
all_modes = tt_totals_for_mode_list(trip_tables, mode_list)

sum_all_modes = all_modes['SOV'] + all_modes['HOV'] +                 all_modes['Heavy_Truck'] + all_modes['Heavy_Truck_HazMat'] +                 all_modes['Medium_Truck'] + all_modes['Medium_Truck_HazMat'] +                 all_modes['Light_Truck'] +                 all_modes['DAT_Boat'] + all_modes['DET_Boat'] +                  all_modes['DAT_CR'] + all_modes['DET_CR'] +                 all_modes['DAT_LB'] + all_modes['DET_LB'] +                 all_modes['DAT_RT'] + all_modes['DET_RT'] +                 all_modes['WAT']


# In[13]:


sum_all_modes_by_origin = sum_all_modes.sum(axis=1)


# In[14]:


# Build a data frame, indexed by omxid, containing the  trips originating in each TAZ:
total_all_modes_trips_df = pd.DataFrame(sum_all_modes_by_origin, columns=['sum_all_modes_by_origin'])
# Set the data frame's index to the omxid of each row, i.e., its index
total_all_modes_trips_df['omxid'] = total_all_modes_trips_df.index
total_all_modes_trips_df.set_index('omxid')


# In[15]:


# A bit of a digression here, for the time being...
# Load the candidate canonical TAZ shapefile as a geopands dataframe
taz_shapefile = taz_shapefile_base_dir + 'candidate_CTPS_TAZ_STATEWIDE_2019.shp'
taz_gdf = gp.read_file(taz_shapefile)
taz_gdf.set_index("id")


# In[16]:


# Add a 'omxid' column to the TAZ geodataframe, and 'calc' in the corresponding omxid value,
# in prep for joining with the total trips dataframe.
taz_gdf['omxid'] = taz_gdf.apply(lambda row: taz_to_omxid[row.id], axis=1)


# In[17]:


# Join the shapefile geodataframe to the total trips dataframe on 'omxid'
joined_df = taz_gdf.join(total_all_modes_trips_df.set_index('omxid'), on='omxid')


# In[18]:


# Extract the rows for external TAZes:
#
# *** WARNING - TEMPORARY HACK HERE !!! ***
#
first_external_taz = 209001
external_taz_gdf = joined_df[joined_df['id'] >= first_external_taz]


# In[19]:


external_taz_gdf


# In[24]:


# Make a static horizontal bar chart of the data
temp_df = external_taz_gdf[['id', 'town_state','sum_all_modes_by_origin']]
temp_df = temp_df.rename(columns={'sum_all_modes_by_origin' : 'total_demand'})
#
plt.rcParams["figure.figsize"] = (10,20)
#
temp_df.plot.barh(x='id', 
                  y='total_demand', 
                  xlabel='TAZ ID',
                  ylabel='Number of Trips', 
                  title='Number of Trips from External TAZes')


# In[25]:


# Make an interactive bar chart of the same information 
temp_df.hvplot.barh(x='id', 
                    xlabel='Origin TAZ', 
                    y='total_demand', 
                    ylabel='Total Demand', 
                    xformatter="%f", 
                    hover_cols='all',
                    frame_width=500,
                    frame_height=1000)


# In[ ]:




