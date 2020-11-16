#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:42:31 2020

@author: jackreid
"""

import csv
import dateutil
from dateutil import rrule
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np


metrics = ['date',
            'SO2',
            'NO2',
            'NOx',
            'PM10']

datadict = dict()

for metric in metrics:
    datadict[metric] = list()


#Open the CSV with that I manually cut down to approximately the relevant dates
with open('/home/jackreid/Downloads/DailyAirQuality.csv') as csvfile:
    csvread = csv.DictReader(csvfile)
    for row in csvread:
        for metric in metrics:
            if metric == 'date':
                datadict[metric].append(dateutil.parser.parse(row[metric]))
            else:
                if row[metric] != '[]':
                    datadict[metric].append(float(row[metric]))
                else:
                    datadict[metric].append(np.nan)
          

plt.rcParams.update({'font.size': 32})
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 

fig, ax1 = plt.subplots(nrows=2, ncols=2, sharex=True, figsize=(30, 20))

ax1[0,0].plot(datadict['date'],datadict['SO2'])
ax1[0,0].set_title('SO2')
ax1[0,0].set_ylabel('µg/m3')

ax1[0,1].plot(datadict['date'],datadict['NO2'])
ax1[0,1].set_title('NO2')
ax1[0,0].set_ylabel('µg/m3')

ax1[1,0].plot(datadict['date'],datadict['NOx'])
ax1[1,0].set_title('NOx')
ax1[0,0].set_ylabel('µg/m3')

ax1[1,1].plot(datadict['date'],datadict['PM10'])
ax1[1,1].set_title('PM10')
ax1[0,0].set_ylabel('µg/m3')

# ax1.set_ylabel('µg/m3')
# ax1.set_xlabel('Date')

# fig, ax1 = plt.subplots()

# ax1.plot(datadict['date'],datadict['SO2'])
# ax1.set_title('SO2')




# ax1.legend(loc='upper right')
# ax1.set_ylim(vismin, vismax)
# endtime = max(self.timeSeries[-1], 200)
# ax1.set_xlim(0, endtime)
# ax1.set_ylabel(metric)
# ax1.set_xlabel('days')
# fig.tight_layout()