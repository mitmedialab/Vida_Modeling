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
import dateutil
import scipy
from scipy import stats
from datetime import datetime, timedelta
from dateutil import rrule
from screeninfo import get_monitors

#Set filepath of data and location names
filepath = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Auxilary Files/SummaryGraphs/Santiago/Weekly_Median_TS/Nightlights_RelativeAnomaly.csv'
# locations = ['Santos Dumont Airport']
# locations = ['Cidade de Deus', 
#              'Galeao Airport', 
#              'Santos Dumont Airport', 
#              'Industrial Area', 
#              'Pedra de Guaratiba', 
#              'Copacabana', 
#              'Ipanema',
#              'Centro',
#              'Cidade Nova',
#              'Barra da Tijuca',
#              'Campo Grande',
#              'City'
#              ]

#get monitor size for setting plot size
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
                elif entry in ['Date_Name']:
                    date_format =  dateutil.parser.parse(row[entry])
                    newrow[entry] = date_format
            else:
                newrow[entry] = np.nan
        
        datalist.append(newrow)

#Convert data into a DataFrame for plotting purposes
df_data = pd.DataFrame(datalist)

#Sort the DataFrame by date
df_data = df_data[df_data['Week'].notnull()].sort_values(by='Week')

locations = list(row.keys())
locations.remove('Week')
locations.remove('Date_Name')
newlocation=[locations[2]]

#Generate plots and calculate statistics for each location
t_dict = dict()
slopes_dict = dict()
p_norm_dict = dict()
for location in locations:
# for location in newlocation:
    print(location)

    #Set start of pandemic date
    pan_date = dateutil.parser.parse('01 March 2020')
    pan_week = pan_date.date().isocalendar()[1] + 52
    
    #seperate data into pre and post pandemic
    pre_data = df_data[df_data['Week']<pan_week]
    post_data = df_data[df_data['Week']>=pan_week]
    
    #Trends for complete dataset (both pre and post)
    time_loc =df_data['Week'].values
    data_loc = df_data[location].values
    xmask = np.isfinite(data_loc) #Mask nan values
    time_mask = time_loc[xmask]
    data_mask = data_loc[xmask]
    regres = list(scipy.stats.mstats.theilslopes(data_mask, time_mask))    #slope, intercept, lo_slope, up_slope
    poly1d_fn = np.poly1d(regres[0:2]) 
    r,p = scipy.stats.pearsonr(data_mask,poly1d_fn(time_mask))
    regres.append(r)
    regres.append(p)


    #Trends for pre-pandemic data
    time_loc_pre =pre_data['Week'].values
    data_loc_pre = pre_data[location].values
    xmask = np.isfinite(data_loc_pre)
    time_mask_pre = time_loc_pre[xmask]
    data_mask_pre = data_loc_pre[xmask]
    regres_pre = list(scipy.stats.mstats.theilslopes(data_mask_pre, time_mask_pre))
    poly1d_fn_pre = np.poly1d(regres_pre[0:2]) 
    r,p = scipy.stats.pearsonr(data_mask_pre,poly1d_fn_pre(time_mask_pre))
    regres_pre.append(r)
    regres_pre.append(p)

    #Trends for post-pandemic data
    time_loc_post =post_data['Week'].values
    data_loc_post = post_data[location].values
    xmask = np.isfinite(data_loc_post)
    time_mask_post = time_loc_post[xmask]
    data_mask_post = data_loc_post[xmask]
    regres_post = list(scipy.stats.mstats.theilslopes(data_mask_post, time_mask_post))
    poly1d_fn_post = np.poly1d(regres_post[0:2]) 
    r,p = scipy.stats.pearsonr(data_mask_post,poly1d_fn_post(time_mask_post))
    regres_post.append(r)
    regres_post.append(p)

    #Store slope data for later analysis    
    slopes_dict[location] = [regres_pre[0], regres_post[0]]

    #Generate plot of relative anomaly data with trends lines
    fig = plt.figure()
    plt.plot(time_mask,data_mask,'yo',
              time_mask,poly1d_fn(time_mask),'--k', 
              time_mask_pre,poly1d_fn_pre(time_mask_pre),'--r',
              time_loc_post,poly1d_fn_post(time_loc_post),'--g')
    ax = plt.gca()
    ax.legend(('Nightlights Data', 
                'Full Date Range Fit, r2 = ' + str(round(regres[4]**2,3)) + ', p = ' + "{:.2e}".format(regres[5]), 
                'Pre Pandemic Fit, r2 = ' + str(round(regres_pre[4]**2,3)) + ', p = ' + "{:.2e}".format(regres_pre[5]), 
                'Post Pandemic Fit, r2 = ' + str(round(regres_post[4]**2,3)) + ', p = ' + "{:.2e}".format(regres_post[5])
                  ))
    plt.title(location)
    plt.ylabel('Relative Weekly Average Anomaly')
    plt.xlabel ('Week (1 = Start of 2019)')
    
    # plt.show()
    
    
    #Size and save the figure
    plt.figure(num=1, figsize=(775/my_dpi, 440/my_dpi), dpi=my_dpi)
    titlestring = './Santiago/' + location + '_Nightlights' + '.jpg'
    fig.savefig(titlestring, dpi=my_dpi)
    plt.close(fig)
    
    #Conduct T-Test on Pre and Post Datasets
    t_results= scipy.stats.ttest_ind(a = data_mask_pre,
                                      b = data_mask_post,
                                      equal_var = False)
    t_dict[location] = t_results[1]
    
    #Normalize the post-pandemic data based on the pre-pandemic trendline
    pre_norm = poly1d_fn_pre(time_mask_post)
    post_norm = data_mask_post - pre_norm
    
    #Calculate trends for normalized data
    regres_post_norm = list(scipy.stats.mstats.theilslopes(post_norm, time_mask_post))
    poly1d_fn_post_norm = np.poly1d(regres_post_norm[0:2]) 
    r,p = scipy.stats.pearsonr(post_norm,poly1d_fn_post_norm(time_mask_post))
    regres_post_norm.append(r)
    regres_post_norm.append(p)
    
    p_norm_dict[location] = p
    
    
    #Generate plot of normalized data and trend
    fig2 = plt.figure()
    plt.plot(time_mask_post, post_norm, 'yo',
              time_mask_post, poly1d_fn_post_norm(time_mask_post), '--g')
    ax2 = plt.gca()
    plt.title(location + ': Normalized')
    plt.ylabel('Relative Weekly Average Anomaly Minus Pre-Pandemic Trend')
    plt.xlabel('Week (1 = Start of 2019)')
    ax2.legend(('Post Pandemic Noramlized Data',
              'Linear Fit, r2 = ' + str(round(regres_post_norm[4]**2,3)) + ', p = ' + str(round(regres_post_norm[5],3))))
   
    # plt.show()
    
    #Size and save the figure
    plt.figure(num=1, figsize=(775/my_dpi, 440/my_dpi), dpi=my_dpi)
    titlestring = './Santiago/' + location + '_Nightlights_Normalized' + '.jpg'
    fig2.savefig(titlestring, dpi=my_dpi)
    plt.close(fig2)
    
    
#Save CSV of statistical data
filename = './Santiago/' + 'Median_Weekly_TS_Stats' +'.csv'
fields = ['Area',
          'T-Value',
          'Norm_P_Value',
          'PrePVal*1000',
          'PostPVal*1000']

with open(filename,'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    dictlist = []
    for location in locations:
        loc_dict = dict()
        loc_dict['Area'] = location
        loc_dict['T-Value'] = t_dict[location]
        loc_dict['Norm_P_Value'] = p_norm_dict[location]
        loc_dict['PrePVal*1000'] = slopes_dict[location][0] * 1000
        loc_dict['PostPVal*1000'] = slopes_dict[location][1] * 1000
        dictlist.append(loc_dict)
    writer.writerows(dictlist)         
    
    
    
    