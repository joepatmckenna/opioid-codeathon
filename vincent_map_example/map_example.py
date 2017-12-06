# -*- coding: utf-8 -*-
"""

Vincent Map Examples

"""

#Build a map from scratch

from vincent import *

world_topo = r'world-countries.topo.json'
state_topo = r'us_states.topo.json'
lake_topo = r'lakes_50m.topo.json'
county_geo = r'us_counties.geo.json'
county_topo = r'us_counties.topo.json'
or_topo = r'or_counties.topo.json'


#Choropleth
import json
import pandas as pd
#Map the county codes we have in our geometry to those in the
#county_data file, which contains additional rows we don't need
with open('us_counties.topo.json', 'r') as f:
    get_id = json.load(f)

#A little FIPS code munging
new_geoms = []
for geom in get_id['objects']['us_counties.geo']['geometries']:
    geom['properties']['FIPS'] = int(geom['properties']['FIPS'])
    new_geoms.append(geom)

get_id['objects']['us_counties.geo']['geometries'] = new_geoms

with open('us_counties.topo.json', 'w') as f:
    json.dump(get_id, f)

#Grab the FIPS codes and load them into a dataframe
geometries = get_id['objects']['us_counties.geo']['geometries']
county_codes = [x['properties']['FIPS'] for x in geometries]
county_df = pd.DataFrame({'FIPS': county_codes}, dtype=str)
county_df = county_df.astype(int)

#Read into Dataframe, cast to int for consistency
df = pd.read_csv('data/us_county_data.csv', na_values=[' '])
df['FIPS'] = df['FIPS'].astype(int)

#Perform an inner join, pad NA's with data from nearest county
merged = pd.merge(df, county_df, on='FIPS', how='inner')
merged = merged.fillna(method='pad')

geo_data = [{'name': 'counties',
             'url': county_topo,
             'feature': 'us_counties.geo'}]

vis = Map(data=merged, geo_data=geo_data, scale=1100, projection='albersUsa',
          data_bind='Employed_2011', data_key='FIPS',
          map_key={'counties': 'properties.FIPS'})
		  
vis.marks[0].properties.enter.stroke_opacity = ValueRef(value=0.5)
#Change our domain for an even inteager
vis.scales['color'].domain = [0, 189000]
vis.legend(title='Number Employed 2011')
vis.to_json('vega.json', html_out=True, html_path='map_example.html')

#Lets look at different stats
# vis.rebind(column='Civilian_labor_force_2011', brew='BuPu')
# vis.to_json('vega.json', html_out=True, html_path='map_example.html')

# vis.rebind(column='Unemployed_2011', brew='PuBu')
# vis.to_json('vega.json', html_out=True, html_path='map_example.html')

# vis.rebind(column='Unemployment_rate_2011', brew='YlGnBu')
# vis.to_json('vega.json', html_out=True, html_path='map_example.html')

# vis.rebind(column='Median_Household_Income_2011', brew='RdPu')
# vis.to_json('vega.json', html_out=True, html_path='map_example.html')
