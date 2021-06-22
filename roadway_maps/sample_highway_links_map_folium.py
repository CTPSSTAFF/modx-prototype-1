#!/usr/bin/env python
# coding: utf-8

# In[13]:


# Notebook to display data for selected highway links flow, V/C, and speeds using the folium library.
# Data was previously calculated by sample_highway_links_report.ipypnb, and saved in CSV format.

import openmatrix as omx
import numpy as np
import pandas as pd
import geopandas as gp
from io import StringIO
import matplotlib.pyplot as plt
import json
import folium


# In[3]:


# Directory in which user's output CSV report data was saved - it will now be our *input* directory
my_output_dir = r'S:/my_modx_output_dir/'


# In[4]:


# Name of CSV output file with volume, V/C, and speed data for selected links - it will now be our *input* CSV file
csv_output_fn = 'links_report.csv'


# In[5]:


# Fully-qualified pathname to CSV file
fq_output_fn = my_output_dir + csv_output_fn


# In[6]:


links_data_df = pd.read_csv(fq_output_fn, delimiter=',')


# In[7]:


links_data_df


# In[8]:


# Get the list of link IDs
links_list = links_data_df['ID1'].to_list()


# In[12]:


# Load the GeoJSON for the model network links
#
# Directory in which the spatial data for the model network links is stored (both shapefile and GeoJSON formats)
links_spatial_data_dir = r'G:/Data_Resources/modx/statewide_links_shapefile/'
links_geojson_fn = 'Statewide_Links_2018_BK_EPSG26986.geojson'
fq_links_geojson_fn = links_spatial_data_dir + links_geojson_fn
links_geojson_str = open(fq_links_geojson_fn).read()


# In[15]:


# Turn the GeoJSON string into a real GeoJSON data structure
links = json.loads(links_geojson_str)


# In[17]:


len(links['features'])


# In[19]:


# The following statement gets the properties of the feature at index 0.
# The feature ID (link ID) is given by the "ID" property.
links['features'][0]['properties']


# In[52]:


# Filter the list of features (links) to only the links of interest
#
features = links['features']
found_list = []
for feat in features:
    count = count + 1
    if feat['properties']['ID'] in links_list:
        # print('Found ' + str(feat['properties']['ID']))
        found_list.append(feat)
    # end_if
# end_for
links['features'] = found_list


# In[53]:


len(links['features'])


# In[55]:


filtered_links_geojson_string = json.dumps(links)


# In[62]:


filtered_links_geojson_string[0:200]


# In[59]:


#
center = [42.27, -71.73]
m = folium.Map(location=center, zoom_start=8)
folium.GeoJson(filtered_links_geojson_string).add_to(m)


# In[ ]:





# In[ ]:





# In[64]:


## TESTING 1, 2, 3...
tmp_base = r'G:/Data_Resources/DataStore/Ben_Marg_Proto/'
taz_geojson_file = tmp_base + 'candidate_CTPS_TAZ_STATE_2019.geojson'
taz_geojson = open(taz_geojson_file).read()


# In[65]:


taz_geojson[0:100]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




