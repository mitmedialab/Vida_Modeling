#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:39:12 2021

@author: jackreid
"""

import pandas as pd
import numpy as np
import csv

import matplotlib.pyplot as plt 
from screeninfo import get_monitors



#Set filepath of data
filepath = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Luanda/Luanda_graphs.csv'

#Get screen resolution, used for sizing the graphs later on
for m in get_monitors():
    print(str(m))
my_dpi = m.width/(m.width_mm*0.0393701)


#Extract data from the csv
datalist = []
with open(filepath) as csvfile:
    readCSV1 = csv.DictReader(csvfile, delimiter=',')
    for row in readCSV1:
        newrow = dict()
        for entry in row.keys():
            if row[entry]:
                if entry not in ['Date_Name','Policy_Name']:
                    newrow[entry] = float(row[entry])
            else:
                newrow[entry] = np.nan
        
        datalist.append(newrow)

#Convert data into a DataFrame for plotting purposes
df_data = pd.DataFrame(datalist)

#Sort the DataFrame by date
df_data = df_data[df_data['Date'].notnull()].sort_values(by='Date')

#Specify the variables to be compared on the graph. Each variable in the comp1 list will be plotted pairwise against
#each variable in the comp2 list
comp1 = ['Policy','New_Cases_pc']
comp2 = ['Policy','nat_residential_mob','nat_transit_mob']

#Define the colors to be used for each variable, the label on their axis, and their label in the legend)
color_dict = {'Policy' : '#6DFD0D',
              'nat_residential_mob' : '#73FFDF',
              'nat_transit_mob' : '#73FFDF',
              'New_Cases_pc' : '#FF73EE'}

label_dict = {'Policy' : 'Policy (0 = Lockdown, 10 = Open)',
              'nat_residential_mob' : 'Residential Mobility Index',
              'nat_transit_mob' : 'Transit Mobility Index',
              'New_Cases_pc' : 'Daily New Cases per Capita'}

legend_dict = {'Policy' : 'Policy',
              'nat_residential_mob' : 'Residential Mobility',
              'nat_transit_mob' : 'Transit Mobility',
              'New_Cases_pc' : 'Daily New Cases'}

#Generate each plot
for entry1 in comp1:
    for entry2 in comp2:
        
        #Set the appropriate congfiguration for the grid
        plt.rcParams['axes.grid'] = True
        plt.rcParams['axes.grid.which'] = 'both'
        plt.rcParams['xtick.minor.visible'] = False
        plt.rcParams['legend.frameon'] = 'False'
        
        #Plot the first variable
        ax = df_data.plot(kind = 'line', x = 'Date', 
                          y = entry1, color = color_dict[entry1], 
                          linewidth = 1,
                          legend = False) 
        ax.set_facecolor('#222222')
        ax.set_ylabel(label_dict[entry1])
        ax.xaxis.label.set_color('#FFFFFF')
        ax.tick_params(axis='x', colors='#D6D6D6')
        ax.yaxis.label.set_color('#FFFFFF')
        ax.tick_params(axis='y', colors='#D6D6D6')
        
        #Plot the second variable
        ax2 = df_data.plot(kind = 'line', x = 'Date',  
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

        #Generate the figure
        fig = ax.get_figure()
        fig.autofmt_xdate()
        fig.patch.set_facecolor('#222222')
        myLegend = fig.legend(labelcolor = '#FFFFFF', loc='upper center')
        myLegend.get_texts()[0].set_text(legend_dict[entry1])
        myLegend.get_texts()[1].set_text(legend_dict[entry2])

        #Size and save the figure
        plt.figure(num=1, figsize=(775/my_dpi, 440/my_dpi), dpi=my_dpi)
        titlestring = './' + entry1 + '_' + entry2 + '.jpg'
        fig.savefig(titlestring, dpi=my_dpi)
        plt.close(fig)




