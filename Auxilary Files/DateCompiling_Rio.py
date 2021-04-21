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


filepath_covid = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Rio de Janeiro/Misc/Cases_by_Date_Symptoms.json'
with open(filepath_covid) as f:
    data_covid_raw = json.load(f)

data_covid = data_covid_raw['features']
# print(data)
    
vaccine_list = list()
for entry in data_covid:
    attributes = entry['attributes']
    date_int1 = attributes['dt_inicio_sintomas']
    if date_int1:
        date_int1 = int(date_int1)/1000
        date1 = datetime.utcfromtimestamp(date_int1)
        date1 = date1.date()
    else:
        date1 = np.nan
    
    attributes['dt_inicio_sintomas'] = date1
    vaccine_list.append(attributes)
    
filename = './CaseByDate' +'.csv'
fields = vaccine_list[0].keys()
with open(filename,'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(vaccine_list)       