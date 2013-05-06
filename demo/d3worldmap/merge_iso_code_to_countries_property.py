#!/usr/bin/python
# coding: UTF-8

import json

f_cdata = open('countries_from_wikipedia.txt', 'r')
countries = {} 
for line in f_cdata:
    cells = line.strip().split('\t')
    country = None
    country = {'name':cells[1],'japanese':cells[0],'numeric':cells[2]}
    print country 
    countries[cells[3]] = country 

f_topo = open('topo_world_countries.json','r')
json_data = json.loads(f_topo.read())

for i in range(len(json_data['objects']['countries']['geometries'])):
    try:
        json_data['objects']['countries']['geometries'][i]['properties'] = countries[json_data['objects']['countries']['geometries'][i]['id']]
    except:
        pass
result_file = open('topo_world_countries_with_meta.json','w')
result_file.write(json.dumps(json_data, encoding='UTF-8'))
