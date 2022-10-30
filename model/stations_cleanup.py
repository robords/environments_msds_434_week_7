'''
Format of the stations file:

Variable	Columns	Type	Example    
ID	1-11	Character	EI000003980    
LATITUDE	13-20	Real	55.3717    
LONGITUDE	22-30	Real	-7.3400    
ELEVATION	32-37	Real	21.0    
STATE	39-40	Character    
NAME	42-71	Character	MALIN HEAD    
GSN FLAG	73-75	Character	GSN    
HCN/CRN FLAG	77-79	Character    
WMO ID	81-85	Character	03980    
'''

import pandas as pd

colspecs = [(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71), (72, 75), (76, 79), (80, 85)]

station_data = pd.read_fwf('./weather/ghcnd-stations.txt', header=None, colspecs=colspecs,
                           names=['id', 'latitude', 'longitude', 'elevation', 'state', 'name', 'gsn_flag', 'hcn_crn_flag', 'wmo_id'])

station_data_for_model = station_data[['id', 'state']]
station_data_for_model.dropna().to_csv('./weather/stations.csv', index=False)