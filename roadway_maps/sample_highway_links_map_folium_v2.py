#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Notebook to display data for selected highway links flow, V/C, and speeds using the folum library.
# 
# Approach: Load spatial (shapefile) and tabular data into a geodataframe,
#           export the geodataframe to a GeoJSON file,
#           and then load the GeoJSON file into a folium map.
#
# Tabular data was previously calculated by sample_highway_links_report.ipypnb, and saved in CSV format.

import openmatrix as omx
import numpy as np
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
import jenkspy
import folium
# TBD: Add hvplot library for interactive bar charts


# In[7]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[8]:


# Directory in which user's output CSV report data was saved - it will now be our *input* directory
my_sandbox_dir = r'S:/my_modx_output_dir/'


# In[9]:


# Name of CSV file with volume, V/C, and speed data for selected links - it will now be our *input* CSV file
csv_fn = 'links_report_base_scenario.csv'


# In[10]:


# Name of CSV file with volume, V/C, and speed data for selected links - it will now be our *input* CSV file
csv_fn = 'links_report_base_scenario.csv'


# In[11]:


# Fully-qualified pathname to CSV file
fq_csv_fn = my_sandbox_dir + csv_fn


# In[12]:


links_data_df = pd.read_csv(fq_csv_fn, delimiter=',')


# In[13]:


links_data_df


# In[14]:


list(links_data_df.columns)


# In[15]:


# List of the IDs for the model network links for which data is reported in the input CSV file
links_list = links_data_df['ID1'].to_list()


# In[16]:


# Directory in which the spatial data for the model network links is stored (both shapefile and GeoJSON formats)
links_spatial_data_dir = r'G:/Data_Resources/modx/statewide_links_shapefile/'


# In[17]:


# Load the links shapefile into a geopandas dataframe 
# NOTE: This version of the shapefile is in EPSG4326, i.e., WGS84
links_shapefile_fn = 'Statewide_Links_2018_BK_EPSG4326.shp'
fq_links_shapefile_fn = links_spatial_data_dir + links_shapefile_fn
links_gdf = gp.read_file(fq_links_shapefile_fn)
links_gdf.set_index("ID")


# In[18]:


# Filter the links geodataframe to only the links of interest
filtered_links_gdf = links_gdf[links_gdf['ID'].isin(links_list)] 


# In[19]:


filtered_links_gdf


# In[20]:


# Join the geo-data frame for the links with the "links_data_df", which contains the computed data about these links
join_df = filtered_links_gdf.join(links_data_df.set_index("ID1"), on="ID")


# In[21]:


join_df


# In[22]:


# Export the geo-dataframe to GeoJSON format, so it can be used with the folium library
out_geojson_fn = my_sandbox_dir + 'temp_geojson.geojson'
join_df.to_file(out_geojson_fn, driver='GeoJSON')


# In[41]:


# Make a static map of speed during the AM period
join_df.plot("Speed_am", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Speed in AM')
plt.show()


# In[46]:


# Render an interactive folium map of AM speed
# 
# model_region_center = [42.27, -71.73]
#
# For now, we'll use a "canned center value"
# TBD: compute center from GeoJSON
#
center = [42.38439, -71.05103]
m = folium.Map(location=center, zoom_start=12)
links_geojson = open(out_geojson_fn).read()
#
def colorscale(speed):
    if (speed > 50.0):
        retval = '#yellow'
    elif (speed > 40.0):
        retval = '#goldenrod'
    elif (speed > 30.0):
        retval = '#e56a5d'
    elif (speed > 20.0):
        retval = '#c13b82'
    elif (speed > 10.0):
        retval = '#8405a7'
    else:
        retval = '#3c0493'
    #
    return retval
#
def my_style_function(feature):
    speed = feature['properties']['Speed_am']
    return {
        'opacity': 1.0,
        'color': colorscale(speed)
    }
#
folium.GeoJson(links_geojson,
               style_function=my_style_function).add_to(m)

#
m


# In[ ]:


# TBD: Make an interactive bar chart of speed for each link in the AM period


# In[ ]:





# In[43]:


# Make a static map of total daily flow (volume) during the AM period
join_df.plot("Tot_Flow_daily", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Daily Total Flow (volume)')
plt.show()


# In[48]:


# TBD: Make an interactive folium map of total daily flow (volume) during the AM period
# 
# model_region_center = [42.27, -71.73]
#
# For now, we'll use a "canned center value"
# TBD: compute center from GeoJSON
#
center = [42.38439, -71.05103]
m = folium.Map(location=center, zoom_start=12)
links_geojson = open(out_geojson_fn).read()
#
# *** TBD: This colorscale function needs more work
#
def colorscale(flow):
    if (flow > 120000.0):
        retval = '#yellow'
    elif (flow > 100000.0):
        retval = '#goldenrod'
    elif (flow > 80000.0):
        retval = '#e56a5d'
    elif (flow > 60000.0):
        retval = '#c13b82'
    elif (flow > 40000.0):
        retval = '#8405a7'
    else:
        retval = '#3c0493'
    #
    return retval
#
def my_style_function(feature):
    flow = feature['properties']['Tot_Flow_daily']
    return {
        'opacity': 1.0,
        'color': colorscale(flow)
    }
#
folium.GeoJson(links_geojson,
               style_function=my_style_function).add_to(m)

#
m


# In[ ]:


# TBD: Make an interactive bar chat of total daily flow (volume) during the AM period


# In[ ]:





# In[44]:


# Make a static map of the volume-to-capacity ratio during the AM period
join_df.plot("VOC_am", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Volume/Capacity Ratio')
plt.show()


# In[49]:


# Make an interactive folium map of the volume-to-capacity ratio during the AM period
# 
# model_region_center = [42.27, -71.73]
#
# For now, we'll use a "canned center value"
# TBD: compute center from GeoJSON
#
center = [42.38439, -71.05103]
m = folium.Map(location=center, zoom_start=12)
links_geojson = open(out_geojson_fn).read()
#
# *** TBD: This colorscale function needs more work
#
def colorscale(voc):
    if (voc > 1.75):
        retval = '#yellow'
    elif (voc > 1.5):
        retval = '#goldenrod'
    elif (voc > 1.0):
        retval = '#e56a5d'
    elif (voc > 0.75):
        retval = '#c13b82'
    elif (voc > 0.5):
        retval = '#8405a7'
    else:
        retval = '#3c0493'
    #
    return retval
#
def my_style_function(feature):
    voc = feature['properties']['VOC_am']
    return {
        'opacity': 1.0,
        'color': colorscale(voc)
    }
#
folium.GeoJson(links_geojson,
               style_function=my_style_function).add_to(m)

#
m


# In[ ]:


# Make an interactive bar chart of the volume-to-capacity ratio during the AM period


# In[ ]:




