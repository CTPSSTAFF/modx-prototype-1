#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Total transit trips notebook

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


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[3]:


# Root directory for MoDX output for "base year" model results.
#
base_scenario_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2016 Scen 00_08March2019_MoDXoutputs/'
#
# Root directory for MoDX output for "comparison scenario" model results.
# 
comparison_scenario_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2040 NB Scen 01_MoDXoutputs/'


# In[4]:


# ===>>>USER INPUT REQUIRED: <<<===
#
# Supply path to root directory of scenario to use for the current run of this notebook:
# 
home_dir = base_scenario_dir


# In[5]:


taz_shapefile_base_dir = r'G:/Data_Resources/modx/canonical_TAZ_shapefile/'


# In[6]:


# trip_tables directory - this really "should" be a subdirectory of the base directory, but is isn't currently.
# The real McCoy - where things should go, and will eventually go
tt_dir = home_dir + 'out/'


# In[7]:


# trip tables OMX file (matrices)
tt_am = tt_dir + 'AfterSC_Final_AM_Tables.omx'
tt_md = tt_dir + 'AfterSC_Final_MD_Tables.omx'
tt_pm = tt_dir + 'AfterSC_Final_PM_Tables.omx'
tt_nt = tt_dir + 'AfterSC_Final_NT_Tables.omx'
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
taz_to_omxid_nt = trip_tables['nt'].mapping('ID')


# In[10]:


# We'll assume that the mapping from TAZ ID to OMX ID doesn't vary by time period.
# We'll use the AM mapping as _the_ mapping for all time periods, pending confirmation.
# 
# TBD: Insert "sanity check" that the 4 mappings on "ID" are identical.
#
taz_to_omxid = taz_to_omxid_am


# In[11]:


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


# Transit mode
all_transit = tt_totals_for_mode_list(trip_tables,[ 'DAT_Boat', 'DET_Boat', 'DAT_CR', 'DET_CR', 
                                                    'DAT_LB', 'DET_LB', 'DAT_RT', 'DET_RT', 'WAT'])
dat_boat = all_transit['DAT_Boat']
det_boat = all_transit['DET_Boat']
dat_cr = all_transit['DAT_CR']
det_cr = all_transit['DET_CR']
dat_lb = all_transit['DAT_LB']
det_lb = all_transit['DET_LB']
dat_rt = all_transit['DAT_RT']
det_rt = all_transit['DET_RT']
wat = all_transit['WAT']
dat_boat_total = dat_boat.sum(axis=1)
det_boat_total = det_boat.sum(axis=1)
dat_cr_total = dat_cr.sum(axis=1)
det_cr_total = det_cr.sum(axis=1)
dat_lb_total = dat_lb.sum(axis=1)
det_lb_total = det_lb.sum(axis=1)
dat_rt_total = dat_rt.sum(axis=1)
det_rt_total = det_rt.sum(axis=1)
wat_total = wat.sum(axis=1)
# Grand total for transit mode
transit_total = dat_boat_total + det_boat_total + dat_cr_total + det_cr_total +                 dat_lb_total + det_lb_total + dat_rt_total + det_rt_total + wat_total


# In[14]:


# Build a data frame, indexed by omxid, containing the total of the following kinds of trips originating in each TAZ:
# auto_trips, truck_trips, non-motorized trips, transit trips, and total trips.
total_transit_trips_df = pd.DataFrame(transit_total, columns=['transit_total']) 
# Set the data frame's index to the omxid of each row, i.e., its index
total_transit_trips_df['omxid'] = total_transit_trips_df.index
total_transit_trips_df.set_index('omxid')


# In[15]:


# Load the candidate canonical TAZ shapefile as a geopands dataframe.
taz_shapefile = taz_shapefile_base_dir + 'candidate_CTPS_TAZ_STATEWIDE_2019_wgs84.shp'
taz_gdf = gp.read_file(taz_shapefile)
taz_gdf.set_index("id")


# In[16]:


# Add a 'omxid' column to the TAZ geodataframe, in prep for joining with the total trips dataframes.
# ==> This also can be done earlier.
taz_gdf['omxid'] = taz_gdf.apply(lambda row: taz_to_omxid[row.id], axis=1)


# In[17]:


# Join the shapefile geodataframe to the total trips dataframe on 'omxid'
joined_df = taz_gdf.join(total_transit_trips_df.set_index('omxid'), on='omxid')


# In[18]:


# Make a static map of total trips by origin TAZ
joined_df.plot('transit_total', figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Total Transit Trips by Origin TAZ')
plt.show()


# In[19]:


# Make an interactive map of the above
joined_df.hvplot(c='transit_total', 
                 geo=True, 
                 hover_cols=['id', 'town', 'transit_total'], 
                 clabel='Total Trips', 
                 cmap='plasma',
                 frame_height=500).opts(title='Total Transit Trips by Origin TAZ')


# In[ ]: