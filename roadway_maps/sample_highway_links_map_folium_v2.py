#!/usr/bin/env python
# coding: utf-8

# In[3]:


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
from io import StringIO
import matplotlib.pyplot as plt
import jenkspy
import folium
import bokeh
import hvplot.pandas


# In[4]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[5]:


# Directory in which user's output CSV report data was saved - it will now be our *input* directory
my_sandbox_dir = r'S:/my_modx_output_dir/'


# In[6]:


# Name of CSV file with volume, V/C, and speed data for selected links - it will now be our *input* CSV file
csv_fn = 'links_report_base_scenario.csv'


# In[7]:


# Name of CSV file with volume, V/C, and speed data for selected links - it will now be our *input* CSV file
csv_fn = 'links_report_base_scenario.csv'


# In[8]:


# Fully-qualified pathname to CSV file
fq_csv_fn = my_sandbox_dir + csv_fn


# In[9]:


links_data_df = pd.read_csv(fq_csv_fn, delimiter=',')


# In[10]:


links_data_df


# In[11]:


list(links_data_df.columns)


# In[12]:


# List of the IDs for the model network links for which data is reported in the input CSV file
links_list = links_data_df['ID1'].to_list()


# In[13]:


# Directory in which the spatial data for the model network links is stored (both shapefile and GeoJSON formats)
links_spatial_data_dir = r'G:/Data_Resources/modx/statewide_links_shapefile/'


# In[14]:


# Load the links shapefile into a geopandas dataframe 
# NOTE: This version of the shapefile is in EPSG4326, i.e., WGS84
links_shapefile_fn = 'Statewide_Links_2018_BK_EPSG4326.shp'
fq_links_shapefile_fn = links_spatial_data_dir + links_shapefile_fn
links_gdf = gp.read_file(fq_links_shapefile_fn)
links_gdf.set_index("ID")


# In[15]:


# Filter the links geodataframe to only the links of interest
filtered_links_gdf = links_gdf[links_gdf['ID'].isin(links_list)] 


# In[16]:


filtered_links_gdf


# In[17]:


# Join the geo-data frame for the links with the "links_data_df", which contains the computed data about these links
join_df = filtered_links_gdf.join(links_data_df.set_index("ID1"), on="ID")


# In[18]:


join_df


# In[19]:


# Export the geo-dataframe to GeoJSON format, so it can be used with the folium library
out_geojson_fn = my_sandbox_dir + 'temp_geojson.geojson'
join_df.to_file(out_geojson_fn, driver='GeoJSON')


# In[20]:


# Make a static map of speed during the AM period
join_df.plot("Speed_am", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Speed in AM')
plt.show()


# In[27]:


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
# Color scale source: https://colorbrewer2.org/#type=diverging&scheme=RdYlGn&n=6 (inverted)
def speed_colorscale(speed):
    if (speed > 50.0):
        retval = '#1a9850'
    elif (speed > 40.0):
        retval = '#91cf60'
    elif (speed > 30.0):
        retval = '#d9ef8b'
    elif (speed > 20.0):
        retval = '#fee08b'
    elif (speed > 10.0):
        retval = '#fc8d59'
    else:
        retval = '#d73027'
    #
    return retval
#
def my_style_function(feature):
    speed = feature['properties']['Speed_am']
    return {
        'opacity': 1.0,
        'weight' : 5.0,
        'color': speed_colorscale(speed)
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


# In[30]:


# Make an interactive folium map of total daily flow (volume) during the AM period
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
# Colorscale source = https://colorbrewer2.org/#type=sequential&scheme=Reds&n=7 (inverted)
def flow_colorscale(flow):
    if (flow > 120000.0):
        retval = '#99000d'
    elif (flow > 100000.0):
        retval = '#cb181d'
    elif (flow > 80000.0):
        retval = '#ef3b2c'
    elif (flow > 60000.0):
        retval = '#fb6a4a'
    elif (flow > 40000.0):
        retval = '#fc9272'
    elif (flow > 20000.0):
        retval = '#fcbba1'
    else:
        retval = '#fee5d9'
    #
    return retval
#
def my_style_function(feature):
    flow = feature['properties']['Tot_Flow_daily']
    return {
        'opacity': 1.0,
        'weight' : 5.0,
        'color': flow_colorscale(flow)
    }
#
folium.GeoJson(links_geojson,
               style_function=my_style_function).add_to(m)

#
m


# In[ ]:


# TBD: Make an interactive bar chat of total daily flow (volume) during the AM period


# In[ ]:





# In[31]:


# Make a static map of the volume-to-capacity ratio during the AM period
join_df.plot("VOC_am", figsize=(10.0,8.0), cmap='plasma', legend=True)
plt.title('Volume/Capacity Ratio')
plt.show()


# In[32]:


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
# # Colorscale source = https://colorbrewer2.org/#type=sequential&scheme=Blues&n=4 (inverted)
def voc_colorscale(voc):
    if (voc > 1.5):
        retval = '#2171b5'
    elif (voc > 1.0):
        retval = '#6baed6'
    elif (voc > 0.5):
        retval = '#bdd7e7'
    else:
        retval = '#eff3ff'
    #
    return retval
#
def my_style_function(feature):
    voc = feature['properties']['VOC_am']
    return {
        'opacity': 1.0,
        'weight' : 5.0,
        'color': voc_colorscale(voc)
    }
#
folium.GeoJson(links_geojson,
               style_function=my_style_function).add_to(m)

#
m


# In[ ]:


# Make an interactive bar chart of the volume-to-capacity ratio during the AM period


# In[ ]:




