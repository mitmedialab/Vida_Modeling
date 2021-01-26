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





filepath_covid = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Santiago/Misc/Graphs/Santiago_graphs.csv'

datalist = []


with open(filepath_covid) as csvfile:
    readCSV1 = csv.DictReader(csvfile, delimiter=',')
    for row in readCSV1:
        newrow = dict()
        for entry in row.keys():
            if entry == 'Date':
                date = dateutil.parser.parse(row[entry])
                date = date.date()
                newrow[entry] = date
            else:
                if row[entry]:
                    newrow[entry] = float(row[entry])
                else:
                    newrow[entry] = np.nan
        
        datalist.append(newrow)


    

df_covid = pd.DataFrame(datalist)

df_covid = df_covid[df_covid['Date'].notnull()].sort_values(by='Date')


comp1 = ['Policy', 'New Cases', 'New Deaths']
comp2 = ['PM10', 'Mobility_Met', 'Mobility_Met_int', 'Mobility_Met_ext']


for entry1 in comp1:
    for entry2 in comp2:
        ax = df_covid.plot(kind = 'line', x = 'Date', 
                          y = entry1, color = 'red', 
                          linewidth = 3) 
          
        ax2 = df_covid.plot(kind = 'line', x = 'Date',  
                            y = entry2, secondary_y = True, 
                            color = 'blue',  linewidth = 3, 
                            ax = ax) 
        fig = ax.get_figure()
        titlestring = './' + entry1 + '_' + entry2 + '.png'
        fig.savefig(titlestring)
        plt.close(fig)




