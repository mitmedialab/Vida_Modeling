#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 15:56:58 2021

@author: jackreid
"""


import urllib.request, json 
import csv
import dateutil
from datetime import datetime
import numpy as np

basename = 'https://services1.arcgis.com/OlP4dGNtIcnD3RYf/ArcGIS/rest/services/db_vacinas_d2/FeatureServer/0/query?where=objectid>'
tail  = '&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token='


data_vaccine = list()
numval = 0
while numval <31000:
    numname = str(numval)
    filename = basename+numname+tail
    with urllib.request.urlopen(filename) as url:
        data_raw = json.loads(url.read().decode())
    data_vaccine = data_vaccine + data_raw['features']
    numval += 2000
    print(numval)
    # print(data)
    
vaccine_list = list()
for entry in data_vaccine:
    attributes = entry['attributes']
    date_int1 = attributes['DATA_APLICACAO']
    if date_int1:
        date_int1 = int(date_int1)/1000
        date1 = datetime.utcfromtimestamp(date_int1)
        date1 = date1.date()
    else:
        date1 = np.nan
    date_int2 = attributes['DATA_ATUALIZACAO']
    if date_int2:
        date_int2 = int(date_int2)/1000
        date2 = datetime.utcfromtimestamp(date_int2)
        date2 = date2.date()
    else:
        date1 = np.nan
    
    attributes['DATA_APLICACAO'] = date1
    attributes['DATA_ATUALIZACAO'] = date2
    vaccine_list.append(attributes)
    
filename = './VaccineData' +'.csv'
fields = vaccine_list[0].keys()
with open(filename,'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(vaccine_list)       