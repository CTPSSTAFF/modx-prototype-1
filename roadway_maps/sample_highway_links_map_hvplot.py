#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Notebook to display data for selected highway links flow, V/C, and speeds using the hvplot library.
# Data was previously calculated by sample_highway_links_report.ipypnb, and saved in CSV format.

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


# In[2]:


# Directory in which user's output CSV report data was saved - it will now be our *input* directory
my_sandbox_dir = r'S:/my_modx_output_dir/'


# In[3]:


# Name of CSV file with volume, V/C, and speed data for selected links - it will now be our *input* CSV file
csv_fn = 'links_report_base_scenario.csv'


# In[4]:


# Fully-qualified pathname to CSV file
fq_csv_fn = my_sandbox_dir + csv_fn


# In[5]:


links_data_df = pd.read_csv(fq_csv_fn, delimiter=',')


# In[6]:


links_data_df


# In[7]:


# Sanity check
list(links_data_df.columns)


# In[8]:


# List of the IDs for the model network links for which data is reported in the input CSV file
links_list = links_data_df['ID1'].to_list()


# In[9]:


# Directory in which the spatial data for the model network links is stored (both shapefile and GeoJSON formats)
links_spatial_data_dir = r'G:/Data_Resources/modx/statewide_links_shapefile/'


# In[10]:


# Load the links shapefile into a geopandas dataframe 
# NOTE: This version of the shapefile is in EPSG4326, i.e., WGS84
links_shapefile_fn = 'Statewide_Links_2018_BK_EPSG4326.shp'
fq_links_shapefile_fn = links_spatial_data_dir + links_shapefile_fn
links_gdf = gp.read_file(fq_links_shapefile_fn)
links_gdf.set_index("ID")


# In[11]:


# Filter the links geodataframe to only the links of interest
filtered_links_gdf = links_gdf[links_gdf['ID'].isin(links_list)] 


# In[12]:


filtered_links_gdf


# In[13]:


# Join the geo-data frame for the links with the "links_data_df", which contains the computed data about these links
join_df = filtered_links_gdf.join(links_data_df.set_index("ID1"), on="ID")


# In[14]:


join_df


# In[24]:


# Make a static map of speed during the AM period
join_df.plot("Speed_am", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Speed in AM')


# In[25]:


# Make a static map of the volume-to-capacity ratio during the AM period
join_df.plot("VOC_am", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('VOC in AM')


# In[26]:


# Make a static map of total daily flow (volume) ratio during the AM period
join_df.plot("Tot_Flow_daily", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Daily Total Flow (volume)')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




