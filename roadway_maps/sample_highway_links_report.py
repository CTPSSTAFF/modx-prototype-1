#!/usr/bin/env python
# coding: utf-8

# In[157]:


# Sample highway links flow, V/C, and speeds notebook

import openmatrix as omx
import numpy as np
import pandas as pd
import geopandas as gp
from io import StringIO
import matplotlib.pyplot as plt
import bokeh
import xarray as xr
import hvplot.pandas
import hvplot.xarray
import cartopy.crs as ccrs
import csv


# In[158]:


# Base directory for MoDX output for "base year" model results.
base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2016 Scen 00_08March2019_MoDXoutputs/'


# In[159]:


# Base directory for MoDX output for "comparison scenario" model results.
# Unused in the current version of this notebook
comparison_base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2040 NB Scen 01_MoDXoutputs/'


# In[160]:


# Directory containing link flow CSVs
link_flow_dir = base_dir + 'out/'


# In[ ]:


# Get the IDs of the links for which to generate this report:
#
# Directory containing CSVs with the IDs of the sample links to use for this prototype
sample_links_dir = r'G:/Data_Resources/modx/sample_model_links/'
#
# CSV files with sample highway and transit links for this prototype
highway_links_csv = sample_links_dir + 'highway_links.csv'
transit_links_csv = sample_links_dir + 'transit_links.csv'
#
# Load the above into dataframes
highway_links_df = pd.read_csv(highway_links_csv, delimiter=",")
transit_links_df = pd.read_csv(transit_links_csv, delimiter=",")
# And convert the column with the link ID in each dataframe to a Python list
#
highway_links_list = highway_links_df['TC_Link_ID'].tolist()
transit_links_list = transit_links_df['Route_ID'].tolist()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[163]:


# Individual link-flow CSV tables:
# For each time period, there is a separate flow CSV for autos and for trucks.
# To get the total volume for any given time period, these need to be summed.
# However, the V/C and speed data for *both* autos and trucks are reported in the CSV for autos.
# Clear?
#
am_flow_auto_fn = link_flow_dir + 'AM_MMA_LinkFlow.csv'
am_flow_truck_fn = link_flow_dir + 'AM_MMA_LinkFlow_Trucks.csv'
#
md_flow_auto_fn = link_flow_dir + 'MD_MMA_LinkFlow.csv'
md_flow_truck_fn = link_flow_dir + 'MD_MMA_LinkFlow_Trucks.csv'
#
pm_flow_auto_fn = link_flow_dir + 'PM_MMA_LinkFlow.csv'
pm_flow_truck_fn = link_flow_dir + 'PM_MMA_LinkFlow_Trucks.csv'
#
nt_flow_auto_fn = link_flow_dir + 'NT_MMA_LinkFlow.csv'
nt_flow_truck_fn = link_flow_dir + 'NT_MMA_LinkFlow_Trucks.csv'


# In[197]:


# Read each of the above CSV files containing flow data into a dataframe
#
temp_am_auto_df = pd.read_csv(am_flow_auto_fn, delimiter=',')
temp_am_truck_df = pd.read_csv(am_flow_truck_fn, delimiter=',')
#
temp_md_auto_df = pd.read_csv(md_flow_auto_fn, delimiter=',')
temp_md_truck_df = pd.read_csv(md_flow_truck_fn, delimiter=',')
#
temp_pm_auto_df = pd.read_csv(pm_flow_auto_fn, delimiter=',')
temp_pm_truck_df = pd.read_csv(pm_flow_truck_fn, delimiter=',')
#
temp_nt_auto_df = pd.read_csv(nt_flow_auto_fn, delimiter=',')
temp_nt_truck_df = pd.read_csv(nt_flow_truck_fn, delimiter=',')


# In[199]:


# Filter the 8 "flow" dataframes to only include rows for the selected highway links
#
am_auto_df = temp_am_auto_df[temp_am_auto_df['ID1'].isin(highway_links_list)]
am_truck_df = temp_am_truck_df[temp_am_truck_df['ID1'].isin(highway_links_list)]
#
md_auto_df = temp_md_auto_df[temp_md_auto_df['ID1'].isin(highway_links_list)]
md_truck_df = temp_md_truck_df[temp_md_truck_df['ID1'].isin(highway_links_list)]
#
pm_auto_df = temp_pm_auto_df[temp_pm_auto_df['ID1'].isin(highway_links_list)]
pm_truck_df = temp_pm_truck_df[temp_pm_truck_df['ID1'].isin(highway_links_list)]
#
nt_auto_df = temp_nt_auto_df[temp_nt_auto_df['ID1'].isin(highway_links_list)]
nt_truck_df = temp_nt_truck_df[temp_nt_truck_df['ID1'].isin(highway_links_list)]


# In[200]:


# Further filter the filetered "flow" datafames to only include the columns containing 'Tot_Flow' (and 'ID1')
# 
am_auto_vol_df = am_auto_df[['ID1', 'Tot_Flow']]
am_truck_vol_df = am_truck_df[['ID1', 'Tot_Flow']]
#
md_auto_vol_df = md_auto_df[['ID1', 'Tot_Flow']]
md_truck_vol_df = md_truck_df[['ID1', 'Tot_Flow']]
#
pm_auto_vol_df = pm_auto_df[['ID1', 'Tot_Flow']]
pm_truck_vol_df = pm_truck_df[['ID1', 'Tot_Flow']]
#
nt_auto_vol_df = nt_auto_df[['ID1', 'Tot_Flow']]
nt_truck_vol_df = nt_truck_df[['ID1', 'Tot_Flow']]


# In[ ]:





# In[188]:





# In[ ]:





# In[ ]:





# In[165]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[166]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[168]:


# Convert these into numpy arrays in preparation for summing 'Tot_Flow'
am_auto_vol_np = am_auto_vol_df.to_numpy()
am_truck_vol_np = am_auto_vol_df.to_numpy()
#
md_auto_vol_np = md_auto_vol_df.to_numpy()
md_truck_vol_np = md_truck_vol_df.to_numpy()
#
pm_auto_vol_np = pm_auto_vol_df.to_numpy()
pm_truck_vol_np = pm_truck_vol_df.to_numpy()
#
nt_auto_vol_np = nt_auto_vol_df.to_numpy()
nt_truck_vol_np = nt_truck_vol_df.to_numpy()


# In[186]:


# Get the total volume for each time period
am_auto_vol_np = am_auto_vol_np + am_truck_vol_np
md_total_vol_np = md_auto_vol_np + md_truck_vol_np
pm_total_vol_np = pm_auto_vol_np + pm_truck_vol_np
nt_total_vol_np = nt_auto_vol_np + nt_truck_vol_np


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[172]:


# Sum these 4 arrays to get the total daily flow (and ID1 now muliplied by 8 - eight-fold ugh!)
total_vol_np = am_total_vol_np + md_total_vol_np + pm_total_vol_np + nt_total_vol_np


# In[ ]:





# In[ ]:





# In[151]:


# Convert this to a pandas dataframe
total_vol_df = pd.DataFrame(total_vol_np, columns=['Link_ID_scaled', 'Total_Volume'])


# In[173]:


# Calculate the 'real' link ID for each row
total_vol_df['Link_ID'] = total_vol_df['Link_ID_scaled']/8


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[103]:


# Read each of the link flow CSVs into Python lists - these will be converted to numpy arrays later
#
# AM flow
#
temp_list = []
with open(am_flow_fn, newline='') as csvfile:
    myreader = csv.reader(csvfile, delimiter=',')
    for row in myreader:
        temp_list.append(row)
#
# Save the column names in a separate list, and remove them from 'temp_list'
column_names = temp_list[0]
temp_list.pop(0)
pass


# In[107]:


# Convert all the data to floating point type, so it can be loaded into a numpy array
#
r_ix = 0
retval_list = []
for r in temp_list:
    r_ix += 1
    new_row = []
    # print("Row = " + str(r_ix))
    c_ix = 0
    for c in r:
        c_ix += 1
        # *** WARNING: HACK! to work around cells with no data
        temp = float(c) if c != '' else 0.0
        new_row.append(temp)
    #
    retval_list.append(new_row)
#

# Load retval_list into a numpy array
temp_np = np.array(retval_list)


# In[ ]:





# In[111]:


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


# In[ ]:




