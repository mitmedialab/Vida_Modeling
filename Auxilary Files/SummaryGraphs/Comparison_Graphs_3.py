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
Location = 'Angola'
filepaths = {'Indonesia' : '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Indonesia/Indonesia_graphsV3.csv',
             'Angola': '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Luanda/Luanda_graphs.csv',
             'Queretaro' : '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Querétaro/Queretaro_graphs.csv',
             'Rio de Janeiro': '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Rio de Janeiro/Rio_graphs_Date.csv',
             'Metropolitana': '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Santiago/Metropolitana_graphs.csv'}

transit_title = {'Indonesia' : 'transit_stations_mob',
             'Angola': 'nat_transit_mob',
             'Queretaro' : 'loc_transit_mob',
             'Rio de Janeiro': 'transit_stations_mob',
             'Metropolitana': 'transit_stations_mob'}

filepath = filepaths[Location]

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
                if entry != 'Closure Policy Name' and entry not in ['Date_Name','Policy_Name']:
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
comp1 = 'New_Cases_pc'
comp2 = transit_title[Location]
comp3 = 'Policy'

#Define the colors to be used for each variable, the label on their axis, and their label in the legend)
color_dict = {'Policy' : '#FFF700',
              'nat_residential_mob' : '#73FFDF',
              'loc_transit_mob' : '#73FFDF',
              'nat_transit_mob' : '#73FFDF',
              'transit_stations_mob' : '#73FFDF',
              'New_Cases_pc' : '#FF73EE'}

label_dict = {'Policy' : 'Policy (0 = Lockdown, 10 = Open)',
              'nat_residential_mob' : 'Residential Mobility Index',
              'loc_transit_mob' : 'Transit Mobility Index',
              'nat_transit_mob' : 'Transit Mobility Index',
               'transit_stations_mob' : 'Transit Mobility Index',
              'New_Cases_pc' : 'Daily New Cases per Capita'}

legend_dict = {'Policy' : 'Policy',
              'nat_residential_mob' : 'Residential Mobility',
              'loc_transit_mob' : 'Transit Mobility',
               'nat_transit_mob' : 'Transit Mobility',
               'transit_stations_mob' : 'Transit Mobility',
              'New_Cases_pc' : 'Daily New Cases'}

#Generate each plot




fig, ax = plt.subplots()
ax3 = ax.twinx()
rspine = ax3.spines['right']
rspine.set_position(('axes', 1.15))
ax3.set_frame_on(True)
ax3.patch.set_visible(False)
fig.subplots_adjust(right=0.7)

# #Set the appropriate congfiguration for the grid
plt.rcParams['axes.grid'] = False
plt.rcParams['axes.grid.which'] = 'both'
plt.rcParams['xtick.minor.visible'] = False
plt.rcParams['legend.frameon'] = 'True'

df_data.plot(kind = 'line', x = 'Date', 
                  y = comp1, color = color_dict[comp1], 
                  linewidth = 1,
                  legend = False,
                  ax=ax) 

ax2 = df_data.plot(kind = 'line', x = 'Date',  
                    y = comp2, secondary_y = True, 
                    color = color_dict[comp2],  linewidth = 1, 
                    ax = ax,
                    legend = False) 

df_data.plot(kind = 'line', x = 'Date',  
                    y = comp3, 
                    color = color_dict[comp3],  linewidth = 1, 
                    ax = ax3,
                    legend = False) 


ax.set_facecolor('#222222')
ax.set_ylabel(label_dict[comp1])
ax.xaxis.label.set_color('#FFFFFF')
ax.tick_params(axis='x', colors='#D6D6D6')
ax.yaxis.label.set_color('#FFFFFF')
ax.tick_params(axis='y', colors='#D6D6D6')

ax2.set_facecolor('#222222')
ax2.set_ylabel(label_dict[comp2])
ax2.xaxis.label.set_color('#FFFFFF')
ax2.tick_params(axis='x', colors='#D6D6D6')
ax2.yaxis.label.set_color('#FFFFFF')
ax2.tick_params(axis='y', colors='#D6D6D6')

ax3.set_facecolor('#222222')
ax3.set_ylim([0,11])
ax3.set_ylabel(label_dict[comp3])
ax3.xaxis.label.set_color('#FFFFFF')
ax3.tick_params(axis='x', colors='#D6D6D6')
ax3.yaxis.label.set_color('#FFFFFF')
ax3.tick_params(axis='y', colors='#D6D6D6')



legend_location = {'Indonesia' : (0.4, 1),
             'Angola': (0.5, 0.9),
             'Queretaro' : (0.5, 0.9),
             'Rio de Janeiro': (0.45, 0.9),
             'Metropolitana': (0.71, 0.9)}

fig.patch.set_facecolor('#222222')
myLegend = fig.legend(labelcolor = '#000000', bbox_to_anchor=legend_location[Location])
myLegend.get_texts()[0].set_text(legend_dict[comp1])
myLegend.get_texts()[1].set_text(legend_dict[comp3])
myLegend.get_texts()[2].set_text(legend_dict[comp2])




#Generate the figure
fig = ax.get_figure()
fig.autofmt_xdate()



#Size and save the figure
fig.set_size_inches(8, 5)
# plt.figure(num=1, figsize=(1200/my_dpi, 440/my_dpi), dpi=my_dpi)
titlestring = './' + Location + '3' + '.jpg'
fig.savefig(titlestring, dpi=my_dpi)
plt.close(fig)




