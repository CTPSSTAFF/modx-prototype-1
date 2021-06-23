#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Compare total nonmotorized trips from two scenarios notebook

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


# In[2]:


# Root directory for MoDX output for "base year" model results.
base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2016 Scen 00_08March2019_MoDXoutputs/'


# In[3]:


# Root directory for MoDX output for "comparison scenario" model results.
comparison_base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2040 NB Scen 01_MoDXoutputs/'


# In[4]:


taz_shapefile_base_dir = r'G:/Data_Resources/modx/canonical_TAZ_shapefile/'


# In[5]:


# trip_tables directories 
base_tt_dir = base_dir + 'out/'
comp_tt_dir = comparison_base_dir + 'out/'


# In[6]:


# trip tables OMX file (matrices) for base scenario
base_tt_am = base_tt_dir + 'AfterSC_Final_AM_Tables.omx'
base_tt_md = base_tt_dir + 'AfterSC_Final_MD_Tables.omx'
base_tt_pm = base_tt_dir + 'AfterSC_Final_PM_Tables.omx'
base_tt_nt = base_tt_dir + 'AfterSC_Final_NT_Tables.omx'
base_trip_tables = { 'am' :  omx.open_file(base_tt_am, 'r'),
                     'md' : omx.open_file(base_tt_pm, 'r'),
                     'pm' : omx.open_file(base_tt_pm,'r'),
                     'nt'  : omx.open_file(base_tt_nt, 'r') }


# In[7]:


# trip tables OMX file (matrices) for comparison scenario
comp_tt_am = comp_tt_dir + 'AfterSC_Final_AM_Tables.omx'
comp_tt_md = comp_tt_dir + 'AfterSC_Final_MD_Tables.omx'
comp_tt_pm = comp_tt_dir + 'AfterSC_Final_PM_Tables.omx'
comp_tt_nt = comp_tt_dir + 'AfterSC_Final_NT_Tables.omx'
comp_trip_tables = { 'am' :  omx.open_file(base_tt_am, 'r'),
                     'md' : omx.open_file(base_tt_pm, 'r'),
                     'pm' : omx.open_file(base_tt_pm,'r'),
                     'nt'  : omx.open_file(base_tt_nt, 'r') }


# In[8]:


# trip tables OMX file (matrices) for comparison scenario
comp_tt_am = comp_tt_dir + 'AfterSC_Final_AM_Tables.omx'
comp_tt_md = comp_tt_dir + 'AfterSC_Final_MD_Tables.omx'
comp_tt_pm = comp_tt_dir + 'AfterSC_Final_PM_Tables.omx'
comp_tt_nt = comp_tt_dir + 'AfterSC_Final_NT_Tables.omx'
comp_trip_tables = { 'am' :  omx.open_file(comp_tt_am, 'r'),
                     'md' :  omx.open_file(comp_tt_pm, 'r'),
                     'pm' :  omx.open_file(comp_tt_pm,'r'),
                     'nt'  : omx.open_file(comp_tt_nt, 'r') }


# In[9]:


num_tazes = base_trip_tables['am'].shape()[0]


# In[10]:


# Mapping from TAZ-ID to OMX index for the 4 periods.
# These *should* be the same regardless of time period.
taz_to_omxid_am = base_trip_tables['am'].mapping('ID')
taz_to_omxid_am = base_trip_tables['md'].mapping('ID')
taz_to_omxid_pm = base_trip_tables['pm'].mapping('ID')
taz_to_omxid_nt = base_trip_tables['nt'].mapping('ID')
# Moreover, they should be the same across the two scenarios.
# We'll assume that the mapping from TAZ ID to OMX ID doesn't vary by time period or between scenarios.
# We'll use the AM mapping from the base scenario as _the_ mapping for all time periods, pending confirmation.
#
# *** TBD: Insert "sanity check" that all 8 mappings are identical
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


# Non-motorized mode - base scenario
base_all_nm = tt_totals_for_mode_list(base_trip_tables, ['Bike', 'Walk'])
base_bike = base_all_nm['Bike']
base_walk = base_all_nm['Walk']
base_bike_total = base_bike.sum(axis=1)
base_walk_total = base_walk.sum(axis=1)
# Grand total for the 'non-motorized' mode, base scenario
base_nm_total = base_bike_total + base_walk_total


# In[15]:


# Non-motorized mode - comparison scenario
comp_all_nm = tt_totals_for_mode_list(comp_trip_tables, ['Bike', 'Walk'])
comp_bike = comp_all_nm['Bike']
comp_walk = comp_all_nm['Walk']
comp_bike_total = comp_bike.sum(axis=1)
comp_walk_total = base_walk.sum(axis=1)
# Grand total for the 'non-motorized' mode, comparison scenario
comp_nm_total = comp_bike_total + comp_walk_total


# In[16]:


# Compute delta between scenarios
delta_total_nm = comp_nm_total - base_nm_total


# In[17]:


# Build a data frame, indexed by omxid, 
# containing the delta (between the 2 scenarios) of the total auto trips originating in each TAZ:
delta_total_nm_trips_df = pd.DataFrame(delta_total_nm, columns=['delta_total_nm'])
# Set the data frame's index to the omxid of each row, i.e., its index
delta_total_nm_trips_df['omxid'] = delta_total_nm_trips_df.index
delta_total_nm_trips_df.set_index('omxid')


# In[18]:


# Load the candidate canonical TAZ shapefile as a geopands dataframe.
taz_shapefile = taz_shapefile_base_dir + 'candidate_CTPS_TAZ_STATEWIDE_2019_wgs84.shp'
taz_gdf = gp.read_file(taz_shapefile)
taz_gdf.set_index("id")


# In[19]:


# Add a 'omxid' column to the TAZ geodataframe, in prep for joining with the total trips dataframes.
# ==> This also can be done earlier.
taz_gdf['omxid'] = taz_gdf.apply(lambda row: taz_to_omxid[row.id], axis=1)


# In[20]:


# Join the shapefile geodataframe to the total trips dataframe on 'omxid'
joined_df = taz_gdf.join(delta_total_nm_trips_df.set_index('omxid'), on='omxid')


# In[21]:


# Make a static map of total auto trips by origin TAZ
joined_df.plot("delta_total_nm", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Change in Total Non-motorized Trips by Origin TAZ')


# In[22]:


# Make an interactive map of the above
joined_df.hvplot(c='delta_total_nm', geo=True, hover_cols=['id', 'town', 'delta_total_nm'], 
    clabel='Change in Total Non-motorized Trips', cmap='plasma').opts(title='Change in Total Non-Motorized Trips by Origin TAZ')


# In[ ]:




