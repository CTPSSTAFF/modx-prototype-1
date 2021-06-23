#!/usr/bin/env python
# coding: utf-8

# In[34]:


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


# In[35]:


# Base directory for MoDX output for "base year" model results.
base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2016 Scen 00_08March2019_MoDXoutputs/'


# In[36]:


# Base directory for MoDX output for "comparison scenario" model results.
# Unused in the current version of this notebook
comparison_base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2040 NB Scen 01_MoDXoutputs/'


# In[37]:


# Directory containing link flow CSVs
link_flow_dir = base_dir + 'out/'


# In[38]:


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


# In[39]:


# Individual link-flow CSV tables:
# For each time period, there is a separate flow CSV for autos and for trucks.
# To get the total volume for any given time period, 'Tot_Flow' columns these need to be summed.
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


# In[40]:


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


# In[41]:


# Filter the 8 temp "flow" dataframes to only include rows for the selected highway links
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
#
# NOTE: volume/capacity and speed data will be harvested from the "auto" dataframes subsequently.
#       See below.


# In[42]:


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


# In[43]:


# Rename the 'Tot_Flow' column of each dataframe, appropriately
#
am_auto_vol_df = am_auto_vol_df.rename(columns={'Tot_Flow' : 'Tot_Flow_am_auto'})
am_truck_vol_df = am_truck_vol_df.rename(columns={'Tot_Flow' : 'Tot_Flow_am_truck'})
#
md_auto_vol_df = md_auto_vol_df.rename(columns={'Tot_Flow' : 'Tot_Flow_md_auto'})
md_truck_vol_df = md_truck_vol_df.rename(columns={'Tot_Flow' : 'Tot_Flow_md_truck'})
#
pm_auto_vol_df = pm_auto_vol_df.rename(columns={'Tot_Flow' : 'Tot_Flow_pm_auto'})
pm_truck_vol_df = pm_truck_vol_df.rename(columns={'Tot_Flow' : 'Tot_Flow_pm_truck'})
#
nt_auto_vol_df = nt_auto_vol_df.rename(columns={'Tot_Flow' : 'Tot_Flow_nt_auto'})
nt_truck_vol_df = nt_truck_vol_df.rename(columns={'Tot_Flow' : 'Tot_Flow_nt_truck'})


# In[45]:


# Index all the "volume" dataframes on "ID1", in preparation for joining
#
am_auto_vol_df.set_index("ID1")
am_truck_vol_df.set_index("ID1")
#
md_auto_vol_df.set_index("ID1")
md_truck_vol_df.set_index("ID1")
#
pm_auto_vol_df.set_index("ID1")
pm_truck_vol_df.set_index("ID1")
#
nt_auto_vol_df.set_index("ID1")
nt_truck_vol_df.set_index("ID1")


# In[46]:


# Join the "volume" dataframes
j1_df = am_auto_vol_df.join(am_truck_vol_df.set_index("ID1"), on="ID1")
#
j1_df.set_index("ID1")
j2_df = j1_df.join(md_auto_vol_df.set_index("ID1"), on="ID1")
#
j2_df.set_index("ID1")
j3_df = j2_df.join(md_truck_vol_df.set_index("ID1"), on="ID1")
#
j3_df.set_index("ID1")
j4_df = j3_df.join(pm_auto_vol_df.set_index("ID1"), on="ID1")
#
j4_df.set_index("ID1")
j5_df = j4_df.join(pm_truck_vol_df.set_index("ID1"), on="ID1")
#
j5_df.set_index("ID1")
j6_df = j5_df.join(nt_auto_vol_df.set_index("ID1"), on="ID1")
#
j6_df.set_index("ID1")
total_flow_join = j6_df.join(nt_truck_vol_df.set_index("ID1"), on="ID1")
#
total_flow_join.set_index("ID1")


# In[47]:


# Calculate the total volume (auto + truck) for each time period, and for the entire day
#
total_flow_join['Tot_Flow_am'] = total_flow_join['Tot_Flow_am_auto'] + total_flow_join['Tot_Flow_am_truck']
#
total_flow_join['Tot_Flow_md'] = total_flow_join['Tot_Flow_md_auto'] + total_flow_join['Tot_Flow_md_truck']
#
total_flow_join['Tot_Flow_pm'] = total_flow_join['Tot_Flow_pm_auto'] + total_flow_join['Tot_Flow_pm_truck']
#
total_flow_join['Tot_Flow_nt'] = total_flow_join['Tot_Flow_nt_auto'] + total_flow_join['Tot_Flow_nt_truck']
#
total_flow_join['Tot_Flow_daily'] = total_flow_join['Tot_Flow_am'] + total_flow_join['Tot_Flow_md'] +                                     total_flow_join['Tot_Flow_pm'] + total_flow_join['Tot_Flow_nt']


# In[48]:


# Sanity check
total_flow_join


# In[49]:


total_flow_join.set_index("ID1")


# In[50]:


# Harvest the speed and volume-to-capacity ratio data from the 4 "auto" dataframes, one for each time period. (See above.)
# Note Python variable naming convention used here: "svc" == "speed and volume/capacity"
#
am_svc_df = am_auto_df[['ID1', 'AB_Speed', 'BA_Speed', 'AB_VOC', 'BA_VOC']]
#
md_svc_df = md_auto_df[['ID1', 'AB_Speed', 'BA_Speed', 'AB_VOC', 'BA_VOC']]
#
pm_svc_df = pm_auto_df[['ID1', 'AB_Speed', 'BA_Speed', 'AB_VOC', 'BA_VOC']]
#
nt_svc_df = nt_auto_df[['ID1', 'AB_Speed', 'BA_Speed', 'AB_VOC', 'BA_VOC']]


# In[52]:


# Sanity check
am_svc_df


# In[53]:


# Rename the columns of these "svc" dataframes in preparation for joining them with the speed dataframe, computed above.
#
am_svc_df = am_svc_df.rename(columns={'AB_Speed' : 'AB_Speed_am', 
                                      'BA_Speed' : 'BA_Speed_am',
                                      'AB_VOC'   : 'AB_VOC_am', 
                                      'BA_VOC'   : 'BA_VOC_am'})
#
md_svc_df = md_svc_df.rename(columns={'AB_Speed' : 'AB_Speed_md', 
                                      'BA_Speed' : 'BA_Speed_md',
                                      'AB_VOC'   : 'AB_VOC_md', 
                                      'BA_VOC'   : 'BA_VOC_md'})
#
pm_svc_df = pm_svc_df.rename(columns={'AB_Speed' : 'AB_Speed_pm', 
                                      'BA_Speed' : 'BA_Speed_pm',
                                      'AB_VOC'   : 'AB_VOC_pm', 
                                      'BA_VOC'   : 'BA_VOC_pm'})
#
nt_svc_df = nt_svc_df.rename(columns={'AB_Speed' : 'AB_Speed_nt', 
                                      'BA_Speed' : 'BA_Speed_nt',
                                      'AB_VOC'   : 'AB_VOC_nt', 
                                      'BA_VOC'   : 'BA_VOC_nt'})


# In[54]:


# Sanity check
nt_svc_df


# In[58]:


# Per instructions from Marty on June 22, 2021:
# For a given time period, calculate the MIN of the AB_Speed and BA_Speed, and the MAX of the AB_VOC and BA_VOC.
# Basically, the idea is to flag the link direction with the most congestion.
#
am_svc_df['Speed_am'] = am_svc_df.apply(lambda x: min(x['AB_Speed_am'], x['BA_Speed_am']), axis=1)
am_svc_df['VOC_am'] = am_svc_df.apply(lambda x: max(x['AB_VOC_am'], x['BA_VOC_am']), axis=1)
#
md_svc_df['Speed_md'] = md_svc_df.apply(lambda x: min(x['AB_Speed_md'], x['BA_Speed_md']), axis=1)
md_svc_df['VOC_md'] = md_svc_df.apply(lambda x: max(x['AB_VOC_md'], x['BA_VOC_md']), axis=1)
#
pm_svc_df['Speed_pm'] = pm_svc_df.apply(lambda x: min(x['AB_Speed_pm'], x['BA_Speed_pm']), axis=1)
pm_svc_df['VOC_pm'] = pm_svc_df.apply(lambda x: max(x['AB_VOC_pm'], x['BA_VOC_pm']), axis=1)
#
nt_svc_df['Speed_nt'] = nt_svc_df.apply(lambda x: min(x['AB_Speed_nt'], x['BA_Speed_nt']), axis=1)
nt_svc_df['VOC_nt'] = nt_svc_df.apply(lambda x: max(x['AB_VOC_nt'], x['BA_VOC_nt']), axis=1)


# In[59]:


# Santiy check #1
am_svc_df


# In[60]:


# Santiy check #2
md_svc_df


# In[61]:


# Santiy check #3
pm_svc_df


# In[62]:


# Santiy check #4
nt_svc_df


# In[64]:


# Index the "svc" dataframes in preparation for joining
am_svc_df.set_index("ID1")
md_svc_df.set_index("ID1")
pm_svc_df.set_index("ID1")
nt_svc_df.set_index("ID1")


# In[65]:


# Join the speed and volume/capacity data to the volume data collected above into a single dataframe.
#
j7_df = total_flow_join.join(am_svc_df.set_index("ID1"), on="ID1")
j7_df.set_index("ID1")
#
j8_df = j7_df.join(md_svc_df.set_index("ID1"), on="ID1")
j8_df.set_index("ID1")
#
j9_df = j8_df.join(pm_svc_df.set_index("ID1"), on="ID1")
j9_df.set_index("ID1")
#
all_data_df = j9_df.join(nt_svc_df.set_index("ID1"), on="ID1")
all_data_df.set_index("ID1")


# In[66]:


# Export the dataframe as a CSV file
my_output_dir = r'S:/my_modx_output_dir/'
csv_output_fn = 'links_report_base_scenario.csv'
fq_output_fn = my_output_dir + csv_output_fn
all_data_df.to_csv(fq_output_fn, sep=',')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




