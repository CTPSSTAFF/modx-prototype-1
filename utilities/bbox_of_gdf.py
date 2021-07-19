# bbox_of_gdf.py
# Author: B. Krepp

import pandas as pd
import geopandas as gp

# Return the bounding box of all the features in a geo-dataframe.
# The bounding box is returned as a dictionary with the following keys: { 'minx', 'miny', 'maxx', 'maxy'}.
#
def bbox_of_gdf(gdf):
    bounds_tuples = gdf['geometry'].map(lambda x: x.bounds)
    bounds_dicts = []
    for t in bounds_tuples:
        temp = { 'minx' : t[0], 'miny' : t[1], 'maxx' : t[2], 'maxy' : t[3] }
        bounds_dicts.append(temp)
    # end_for
    bounds_df = pd.DataFrame(bounds_dicts)
    minx = bounds_df['minx'].min()
    miny = bounds_df['miny'].min()
    maxx = bounds_df['maxx'].max()
    maxy = bounds_df['maxy'].max()
    retval = { 'minx' : minx, 'miny' : miny, 'maxx' : maxx, 'maxy' : maxy }
    return retval
# end_def bbox_of_gdf()

# Given a dictonary of the form  'minx', 'miny', 'maxx', 'maxy'} representing a geographic bounding box,
# return the center point as a dictionary with the keys { 'x' , 'y' }.

def center_of_bbox(bbox):
    center_x = bbox['minx'] + (bbox['maxx'] - bbox['minx']) / 2
    center_y = bbox['miny'] + (bbox['maxy'] - bbox['miny']) / 2
    retval = { 'x' : center_x, 'y' : center_y }
    return retval
# end_def center_of_bbox()
