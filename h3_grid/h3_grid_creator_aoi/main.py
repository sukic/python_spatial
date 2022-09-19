# H3 grid API reference: https://h3geo.org/docs/api/indexing (here the version 3.x is used)

# import libraries
import pandas as pd
import geopandas
import h3
from shapely.geometry import Polygon

# paths
in_path = 'inputs/'
out_path = 'outputs/'

#Import the polygon for our area of interest with geopandas
#Can be any of standard geometry formats
gdf = geopandas.read_file(in_path + "h3_bbox_sample.gpkg")


#Get all polygons that intersect our area of interest
#geojson representation of geometry must be used, that is why __geo_interfaca__ is there
hexs = h3.polyfill(gdf.geometry[0].__geo_interface__, 8, geo_json_conformant = True)

# point coordinates table
points = []
for hex_id in hexs:
    points.append([hex_id,h3.h3_to_geo(hex_id)[0],h3.h3_to_geo(hex_id)[1]])

# add to dataframe
df_points = pd.DataFrame(points, columns=["hex_id", "lat", "lng"])




# polygon WKT table
polygons = []
for hex_id in hexs:
    polygons.append([hex_id,Polygon(h3.h3_to_geo_boundary(hex_id,geo_json=True))])


# add to dataframe
df_polygons = pd.DataFrame(polygons, columns=["hex_id", "geometry"])


## exports

df_points.to_csv(out_path + 'points.csv',index=False)
df_polygons.to_csv(out_path + 'polygons.csv',index=False)
