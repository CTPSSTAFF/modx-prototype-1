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
my_output_dir = r'S:/my_modx_output_dir/'


# In[3]:


# Name of CSV output file with volume, V/C, and speed data for selected links - it will now be our *input* CSV file
csv_output_fn = 'links_report.csv'


# In[4]:


# Fully-qualified pathname to CSV file
fq_output_fn = my_output_dir + csv_output_fn


# In[5]:


links_data_df = pd.read_csv(fq_output_fn, delimiter=',')


# In[6]:


links_data_df


# In[7]:


links_list = links_data_df['ID1'].to_list()


# In[8]:


# Directory in which the spatial data for the model network links is stored (both shapefile and GeoJSON formats)
links_spatial_data_dir = r'G:/Data_Resources/modx/statewide_links_shapefile/'


# In[9]:


# Load the links shapefile into a geopandas dataframe 
# NOTE: This version of the shapefile is in EPSG4326, i.e., WGS84
links_shapefile_fn = 'Statewide_Links_2018_BK_EPSG4326.shp'
fq_links_shapefile_fn = links_spatial_data_dir + links_shapefile_fn
links_gdf = gp.read_file(fq_links_shapefile_fn)
links_gdf.set_index("ID")


# In[10]:


# Filter the links geodataframe to only the links of interest
filtered_links_gdf = links_gdf[links_gdf['ID'].isin(links_list)] 


# In[11]:


filtered_links_gdf


# In[12]:


# Join the geo-data frame for the links with the "links_data_df", which contains the computed data about these links
join_df = filtered_links_gdf.join(links_data_df.set_index("ID1"), on="ID")


# In[13]:


join_df


# In[14]:


# Make a static map of the Speed in the A-to-B direction in the AM period
join_df.plot("AB_Speed_am", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('A-B speed in AM')


# In[15]:


# Make an interactive map of the above
join_df.hvplot(geo=True)


# In[ ]:




