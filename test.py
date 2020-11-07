from mvmt.metrics import mvmtMetrics
import math
import geopandas as gp 

path = r'C:\Users\Alexandre\Desktop\PhD\ZOOHACKATHON_2020\DataBase\Multi-species\SHP\etosha_15_elephants.shp'

gp_df = gp.read_file(path)
gp_df = gp_df[gp_df['individu_1']=='LA5']

points = [(a['location-l'],a['location_1']) for i,a in gp_df.iterrows()]
# points = [(1,1),(3,2),(4,3),(3,1),(4,0),(5,1)]

mvmt = mvmtMetrics(points)

