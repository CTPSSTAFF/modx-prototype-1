#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Total auto trips notebook

import openmatrix as omx
import numpy as np
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
import bokeh
import xarray as xr
import hvplot.pandas
import hvplot.xarray
import cartopy.crs as ccrs


# In[3]:


# Based directory for model results.
base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2016 Scen 00_08March2019/' 
#
# For the time being, this is where the trip tables are stored:
fake_base_dir = r'G:/Data_Resources/DataStore/TripTables/'


# In[4]:


# Base directory for model results for comparison.
# NOTE: This variable is unused in the current version of this notebook.
comparison_base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2040 NB Scen 01/'


# In[5]:


taz_shapefile_base_dir = r'G:/Data_Resources/modx/canonical_TAZ_shapefile/'


# In[6]:


# trip_tables directory - this really "should" be a subdirectory of the base directory, but is isn't currently.
# The real McCoy - where things should go, and will eventually go
tt_dir = base_dir + 'out/'
#
# Where things have been put for the time being - ugh
fake_tt_dir = fake_base_dir


# In[7]:


# trip tables OMX file (matrices)
tt_am = fake_tt_dir + 'AfterSC_Final_AM_Tables.omx'
tt_md = fake_tt_dir + 'AfterSC_Final_MD_Tables.omx'
tt_pm = fake_tt_dir + 'AfterSC_Final_PM_Tables.omx'
tt_nt = fake_tt_dir + 'AfterSC_Final_NT_Tables.omx'
trip_tables = { 'am' :  omx.open_file(tt_am, 'r'),
                'md' : omx.open_file(tt_pm, 'r'),
                'pm' : omx.open_file(tt_pm,'r'),
                'nt'  : omx.open_file(tt_nt, 'r') }


# In[8]:


num_tazes = trip_tables['am'].shape()[0]


# In[9]:


# Mapping from TAZ-ID to OMX index for the 4 periods (these *should* be the same)
taz_to_omxid_am = trip_tables['am'].mapping('ID')
taz_to_omxid_am = trip_tables['md'].mapping('ID')
taz_to_omxid_pm = trip_tables['pm'].mapping('ID')
taz_to_omxid_nt =  trip_tables['nt'].mapping('ID')


# In[10]:


# We'll assume that the mapping from TAZ ID to OMX ID doesn't vary by time period.
# We'll use the AM mapping as _the_ mapping for all time periods, pending confirmation.
# 
# TBD: Insert "sanity check" that the 4 mappings on "ID" are identical.
#
taz_to_omxid = taz_to_omxid_am


# In[11]:


# Function tt_total_for_mode
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


# In[12]:


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


# In[13]:


# Auto mode
all_auto = tt_totals_for_mode_list(trip_tables, ['SOV', 'HOV'])
sov = all_auto['SOV']
hov = all_auto['HOV']
sov_total = sov.sum(axis=1)
hov_total = hov.sum(axis=1)
# Grand total for the 'auto' mode
auto_total = sov_total + hov_total


# In[19]:


# Build a data frame, indexed by omxid, containing the total auto trips originating in each TAZ:
total_auto_trips_df = pd.DataFrame(auto_total, columns=['auto_total'])
# Set the data frame's index to the omxid of each row, i.e., its index
total_auto_trips_df['omxid'] = total_auto_trips_df.index
total_auto_trips_df.set_index('omxid')


# In[15]:


# Load the candidate canonical TAZ shapefile as a geopands dataframe.
taz_shapefile = taz_shapefile_base_dir + 'candidate_CTPS_TAZ_STATEWIDE_2019.shp'
taz_gdf = gp.read_file(taz_shapefile)
taz_gdf.set_index("id")


# In[20]:


# Add a 'omxid' column to the TAZ geodataframe, in prep for joining with the total trips dataframes.
# ==> This also can be done earlier.
taz_gdf['omxid'] = taz_gdf.apply(lambda row: taz_to_omxid[row.id], axis=1)


# In[21]:


# Join the shapefile geodataframe to the total trips dataframe on 'omxid'
joined_df = taz_gdf.join(total_auto_trips_df.set_index('omxid'), on='omxid')


# In[22]:


# Make a static map of total auto trips by origin TAZ
joined_df.plot("auto_total", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Total Auito Trips by Origin TAZ')


# In[24]:


# Make an interactive map of the above
joined_df.hvplot(c='auto_total', hover_cols=['id', 'town', 'auto_total'], 
                 clabel='Total Auto Trips', cmap='plasma').opts(title='Total Auto Trips by Origin TAZ')


# In[ ]:




