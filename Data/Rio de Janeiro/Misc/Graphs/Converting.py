#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:39:12 2021

@author: jackreid
"""

import json
import pandas as pd
import numpy as np
import csv
import dateutil
from datetime import datetime
import matplotlib.pyplot as plt 






filepath_covid = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Rio de Janeiro/Misc/Graphs/query.json'
with open(filepath_covid) as f:
    data_covid_raw = json.load(f)

data_covid = data_covid_raw['features']

covid_list = []


phase0_start = dateutil.parser.parse('2020/03/17')
phase1_start = dateutil.parser.parse('2020/06/02')
phase2_start = dateutil.parser.parse('2020/06/17')
phase3a_start = dateutil.parser.parse('2020/07/02')
phase3b_start = dateutil.parser.parse('2020/07/10')
phase4_start = dateutil.parser.parse('2020/07/17')
phase5_start = dateutil.parser.parse('2020/08/01')
phase6a_start = dateutil.parser.parse('2020/09/01')
phase6b_start = dateutil.parser.parse('2020/10/01')
phase7_start = dateutil.parser.parse('2020/11/03')




for entry in data_covid:
    attributes = entry['attributes']
    date_int = attributes['Data']
    if date_int:
        date_int = int(date_int)/1000
        date = datetime.utcfromtimestamp(date_int)
        if date < phase0_start:
            attributes['Policy'] = 10
        elif phase0_start <= date < phase1_start:
            attributes['Policy'] = 0
        elif phase1_start <= date < phase2_start:
            attributes['Policy'] = 1
        elif phase2_start <= date < phase3a_start:
            attributes['Policy'] = 2
        elif phase3a_start <= date < phase3b_start:
            attributes['Policy'] = 3
        elif phase3b_start <= date < phase4_start:
            attributes['Policy'] = 3.5
        elif phase4_start <= date < phase5_start:
            attributes['Policy'] = 4
        elif phase5_start <= date < phase6a_start:
            attributes['Policy'] = 5
        elif phase6a_start <= date < phase6b_start:
            attributes['Policy'] = 6
        elif phase6b_start <= date < phase7_start:
            attributes['Policy'] = 6.5
        elif phase7_start <= date:
            attributes['Policy'] = 7
        date=date.date()
    else:
        date = np.nan
    
    attributes['Date'] = date
    
    covid_list.append(attributes)
    

df_covid = pd.DataFrame(covid_list)

df_covid = df_covid[df_covid['Data'].notnull()].sort_values(by='Date')

df_csv = df_covid.to_csv('./covid_data.csv')






