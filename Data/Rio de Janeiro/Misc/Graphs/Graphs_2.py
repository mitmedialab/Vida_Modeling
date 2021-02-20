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
from screeninfo import get_monitors
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator, LinearLocator, FuncFormatter)

for m in get_monitors():
    print(str(m))


my_dpi = 1920/(193*0.0393701)


filepath_covid = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Rio de Janeiro/Misc/Graphs/Rio_graphs.csv'

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


comp1 = ['Policy', 'New Cases']
comp2 = ['residential_mob', 'transit_stations_mob','Policy']


color_dict = {'Policy' : '#FF73EE',
              'New Cases' : '#FF0000',
              'residential_mob' : '#73FFDF',
              'transit_stations_mob': '#73DFFF'}

label_dict = {'Policy' : 'Policy (0 = Lockdown, 10 = Open)',
              'New Cases' : 'New Cases',
              'residential_mob' : 'Residential Mobility Index',
              'transit_stations_mob': 'Transit Mobility Index'}

legend_dict = {'Policy' : 'Policy',
              'New Cases' : 'New Cases',
              'residential_mob' : 'Residential Mobility',
              'transit_stations_mob': 'Transit Mobility'}

for entry1 in comp1:
    for entry2 in comp2:
        
        plt.rcParams['axes.grid'] = True
        plt.rcParams['axes.grid.which'] = 'both'
        plt.rcParams['xtick.minor.visible'] = False
        plt.rcParams['legend.frameon'] = 'False'
        
        ax = df_covid.plot(kind = 'line', x = 'Date', 
                          y = entry1, color = color_dict[entry1], 
                          linewidth = 1,
                          legend = False) 
        
        ax.set_facecolor('#222222')
        
        # ax.spines['bottom'].set_color('#D6D6D6')
        # ax.spines['top'].set_color('#D6D6D6')
        # ax.spines['left'].set_color('#D6D6D6')
        # ax.spines['right'].set_color('#D6D6D6')
        
        # ax.set_xlabel(label_dict[entry1])
        ax.set_ylabel(label_dict[entry1])
        ax.xaxis.label.set_color('#FFFFFF')
        ax.tick_params(axis='x', colors='#D6D6D6')
        ax.yaxis.label.set_color('#FFFFFF')
        ax.tick_params(axis='y', colors='#D6D6D6')
        
        # ax.legend(labelcolor='#FFFFFF')
        
        # ax.xaxis.set_major_locator(MultipleLocator(20))


        # ax.grid(True)
        # ax.yaxis.grid(True)
        # ax.xaxis.grid(True)
        
        
          
        ax2 = df_covid.plot(kind = 'line', x = 'Date',  
                            y = entry2, secondary_y = True, 
                            color = color_dict[entry2],  linewidth = 1, 
                            ax = ax,
                            legend = False) 
        
        ax2.set_facecolor('#222222')
        
        ax2.set_ylabel(label_dict[entry2])
        ax2.xaxis.label.set_color('#FFFFFF')
        ax2.tick_params(axis='x', colors='#D6D6D6')
        ax2.yaxis.label.set_color('#FFFFFF')
        ax2.tick_params(axis='y', colors='#D6D6D6')
        # ax2.legend(labelcolor='#FFFFFF')
        # legend = ax2.get_legend()
        # legend.get_texts()[0].set_text('make it short')


        
        # ax2.xaxis.set_major_locator(MultipleLocator(20))
        # ax2.yaxis.set_minor_locator(LinearLocator(len(ax.get_yticks())))
        # ax2.yaxis.set_minor_formatter(FuncFormatter(lambda x, pos: '{:0.4f}'.format(x)))
        
        # ax2.grid(True)
        # ax2.yaxis.grid(True)
        # ax2.xaxis.grid(True)

        
        fig = ax.get_figure()
        fig.autofmt_xdate()
        fig.patch.set_facecolor('#222222')
        myLegend = fig.legend(labelcolor = '#FFFFFF', loc='upper center')
        myLegend.get_texts()[0].set_text(legend_dict[entry1])
        myLegend.get_texts()[1].set_text(legend_dict[entry2])

        # myLegend = fig.gca().legend_
        # legend = plt.legend()
        # plt.setp(legend.get_texts(), color='#FFFFFF')
        plt.figure(num=1, figsize=(775/my_dpi, 440/my_dpi), dpi=my_dpi)
        titlestring = './' + entry1 + '_' + entry2 + '.jpg'
        fig.savefig(titlestring, dpi=my_dpi)
        plt.close(fig)




