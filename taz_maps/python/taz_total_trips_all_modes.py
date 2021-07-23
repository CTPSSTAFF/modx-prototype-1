#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# Sanity check #1
trip_tables['am'].list_matrices()


# In[9]:


# Sanity-check #2
trip_tables['am'].list_mappings()


# In[10]:


# Sanity-check #3a
trip_tables['am'].shape()


# In[11]:


# Sanity-check #3b
trip_tables['am'].shape() == trip_tables['md'].shape() == trip_tables['pm'].shape() == trip_tables['nt'].shape()


# In[12]:


# Sanity-check #3c
trip_tables['am'].list_mappings()


# In[13]:


num_tazes = trip_tables['am'].shape()[0]


# In[14]:


# Mapping from TAZ-ID to OMX index for the 4 periods (these *should* be the same)
taz_to_omxid_am = trip_tables['am'].mapping('ID')
taz_to_omxid_am = trip_tables['md'].mapping('ID')
taz_to_omxid_pm = trip_tables['pm'].mapping('ID')
taz_to_omxid_nt =  trip_tables['nt'].mapping('ID')


# In[15]:


# We'll assume that the mapping from TAZ ID to OMX ID doesn't vary by time period.
# We'll use the AM mapping as _the_ mapping for all time periods, pending confirmation.
# 
# TBD: Insert "sanity check" that the 4 mappings on "ID" are identical.
#
taz_to_omxid = taz_to_omxid_am


# In[17]:


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


# In[18]:


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


# In[19]:


# Auto mode
all_auto = tt_totals_for_mode_list(trip_tables, ['SOV', 'HOV'])
sov = all_auto['SOV']
hov = all_auto['HOV']
sov_total = sov.sum(axis=1)
hov_total = hov.sum(axis=1)
# Grand total for the 'auto' mode
auto_total = sov_total + hov_total


# In[20]:


# Truck mode
all_truck = tt_totals_for_mode_list(trip_tables, ['Heavy_Truck', 'Heavy_Truck_HazMat', 
                                                  'Medium_Truck', 'Medium_Truck_HazMat', 'Light_Truck'])
heavy = all_truck['Heavy_Truck']
heavy_haz = all_truck['Heavy_Truck_HazMat']
medium = all_truck['Medium_Truck']
medium_haz = all_truck['Medium_Truck_HazMat']
light = all_truck['Light_Truck']
heavy_total = heavy.sum(axis=1)
heavy_haz_total = heavy_haz_total = heavy_haz.sum(axis=1)
medium_total = medium.sum(axis=1)
medium_haz_total = medium_haz.sum(axis=1)
light_total = light.sum(axis=1)
# Grand total for the 'truck' mode
truck_total = heavy_total + heavy_haz_total + medium_total + medium_haz_total + light_total


# In[21]:


# Non-motorized mode
all_nm = tt_totals_for_mode_list(trip_tables, ['Walk', 'Bike'])
walk = all_nm['Walk']
bike = all_nm['Bike']
walk_total = walk.sum(axis=1)
bike_total = bike.sum(axis=1)
# Grand total for the 'non-motorized' mode
nm_total = walk_total + bike_total


# In[22]:


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
transit_total = dat_boat_total + det_boat_total + dat_cr_total + det_cr_total +               dat_lb_total + det_lb_total + dat_rt_total + det_rt_total + wat_total


# In[23]:


# Grand grand total (i.e., across all modes) of demand by TAZ of origin
grand_total = auto_total + truck_total + nm_total + transit_total


# In[24]:


# Build a data frame, indexed by omxid, containing the total of the following kinds of trips originating in each TAZ:
# auto_trips, truck_trips, non-motorized trips, transit trips, and total trips.
total_trips_df = pd.DataFrame(grand_total, columns=['total_trips'])
total_trips_df['total_auto'] = auto_total
total_trips_df['total_truck'] = truck_total
total_trips_df['total_nm'] = nm_total
total_trips_df['total_transit'] = transit_total 
# Set the data frame's index to the omxid of each row, i.e., its index
total_trips_df['omxid'] = total_trips_df.index
total_trips_df.set_index('omxid')


# In[25]:


# Load the candidate canonical TAZ shapefile as a geopands dataframe.
taz_shapefile = taz_shapefile_base_dir + 'candidate_CTPS_TAZ_STATEWIDE_2019_wgs84.shp'
taz_gdf = gp.read_file(taz_shapefile)
taz_gdf.set_index("id")


# In[26]:


# Add a 'omxid' column to the TAZ geodataframe, in prep for joining with the total trips dataframes.
# ==> This also can be done earlier.
taz_gdf['omxid'] = taz_gdf.apply(lambda row: taz_to_omxid[row.id], axis=1)


# In[27]:


# Join the shapefile geodataframe to the total trips dataframe on 'omxid'
joined_df = taz_gdf.join(total_trips_df.set_index('omxid'), on='omxid')


# In[30]:


# Free as much memory as possible in order to allow the generation of maps and plots to execute
# as quickly as possible, and in some cases, execute at all
#
del all_auto
del all_truck
del all_nm 
del all_transit 


# In[31]:


# Make a static map of total trips by origin TAZ
joined_df.plot("total_trips", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Total Trips by Origin TAZ')
plt.show()

# Make an interactive map to total trips by origin TAZ
joined_df.hvplot(c='total_trips', 
                 geo=True, 
                 hover_cols=['id', 'town_state', 'total_trips'], 
                 clabel='Total Trips', 
                 cmap='plasma',
                 frame_height=500).opts(title='Total Trips by Origin TAZ')

# In[32]:


# Make a static map of total auto trips by origin TAZ
joined_df.plot("total_auto", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Total Auto Trips by Origin TAZ')
plt.show()

# Make an interactive map to total auto trips by origin TAZ
joined_df.hvplot(c='total_auto', 
                      geo=True, 
                      hover_cols=['id', 'town_state', 'total_auto'], 
                      clabel='Total Auto Trips', 
                      cmap='plasma',
                      frame_height=500).opts(title='Total Auto Trips by Origin TAZ')




# In[33]:


# Make a static map of total truck trips by origin TAZ
joined_df.plot("total_truck", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Total Truck Trips by Origin TAZ')
plt.show()

# Make an interactive map to total truck trips by origin TAZ
joined_df.hvplot(c='total_truck', 
                      geo=True, 
                      hover_cols=['id', 'town_state', 'total_truck'], 
                      clabel='Total Truck Trips', 
                      cmap='plasma',
                      frame_height=500).opts(title='Total Truck Trips by Origin TAZ')


# In[34]:


# Make a static map of total non-motorized trips by origin TAZ
joined_df.plot("total_nm", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Total Non-motorized Trips by Origin TAZ')
plt.show()

# Make an interactive map to total non-motorized trips by origin TAZ
joined_df.hvplot(c='total_nm', 
                      geo=True, 
                      hover_cols=['id', 'town_state', 'total_nm'], 
                      clabel='Total Non-motorized Trips', 
                      cmap='plasma',
                      frame_height=500).opts(title='Total Non-motorized Trips by Origin TAZ')


# In[35]:


# Make a static map of total transit trips by origin TAZ
joined_df.plot("total_transit", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Total Transit Trips by Origin TAZ')
plt.show()

# Make an interactive map to total transit trips by origin TAZ
joined_df.hvplot(c='total_transit', 
                      geo=True, 
                      hover_cols=['id', 'town_state', 'total_transit'], 
                      clabel='Total Transit Trips', 
                      cmap='plasma',
                      frame_height=500).opts(title='Total Transit Trips by Origin TAZ')


# In[36]:


# Make a static bar chart of number of trips by mode (mode-share)
# N.B. ttdf == shorthand for total_trips_df
ttdf = total_trips_df
tot_trips = [ttdf['total_auto'].sum() / 10e6, 
             ttdf['total_truck'].sum() / 10e6, 
             ttdf['total_nm'].sum() / 10e6, 
             ttdf['total_transit'].sum() / 10e6]
modes = ['Auto', 'Truck', 'Non-motorized', 'Transit']
temp = { 'modes' : modes, 'total_trips' : tot_trips }
temp_df = pd.DataFrame(temp)


# In[37]:


# Make a bar chart of mode-share according to origin TAZ
temp_df.plot.bar(x='modes', y='total_trips', ylabel='Number of Trips x 10**6', title='Mode Share')


# In[94]:




