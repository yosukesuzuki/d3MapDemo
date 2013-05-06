#!/usr/bin/python
# coding: UTF-8

import json


f = open('countries.geo.json', 'r')
geo_json_data = json.loads(f.read())
#for i in range(len(json_data['features'])):
#    json_data['features'][i]['properties']['id'] = json_data['features'][i]['id']

f_topo = open('topo_world_countries.json','r')
json_data = json.loads(f_topo.read())

for i in range(len(json_data['features'])):
    json_data['features'][i]['properties']['id'] = json_data['features'][i]['id']

result_file = open('topo_world_countries_with_id.json','w')
result_file.write(json.dumps(json_data, encoding='UTF-8'))
