#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 18:25:36 2020

@author: jackreid

This script is the same as AirQualityEditing_Rio_Bairros except it saves all the 
output data in one csv, with a numeric code for each sensor site
"""



import csv
import dateutil
from dateutil import rrule
from datetime import datetime, timedelta
import numpy as np

# =============================================================================
#  Define the initial parameters and setup data structures       
# =============================================================================


#Dictionary of location abbreviations and numeric codes for the relevant bairro
locations = {'CA' : 5,
             'AV' : 24,
             'SC' : 10,
             'SP' : 33,
             'IR' : 76,
             'BG' : 141,
             'CG' : 144,
             'PG' : 153}

#List of metrics as they appear in the raw data csv
metrics = ['Chuva',
           'Pres',
          'RS',
          'Temp',
          'UR',
          'Dir_Vento',
          'Vel_Vento',
          'SO2',
          'NO2',
          'HCNM',
          'HCT',
          'CH4',
          'CO',
          'NO',
          'NOx',
          'O3',
          'PM10',
          'PM2_5']



#Identify dates of interest
startdate = dateutil.parser.parse('2020/03/07 00:00:01+00')
startdate = startdate.date()
enddate = dateutil.parser.parse('2020/06/30 00:00:01+00')
enddate = enddate.date()
dayrange = rrule.rrule(rrule.DAILY, dtstart=startdate, until=enddate)
daylist = []
for day in dayrange:
    daylist.append([day, day+dateutil.relativedelta.relativedelta(days=+1)])


#Set up a dictionary to hold the values: Location->Day->Metric
datadict = dict()

for location in locations.keys():
    datadict[location] = dict()
    for day in daylist:
        datadict[location][day[0].date()] = dict()
        datadict[location][day[0].date()]['date'] = day[0].date()
        for metric in metrics:
            datadict[location][day[0].date()][metric] = []

#Make a copy of dictionary to hold the daily averages
daydict = datadict.copy()
        
filepath = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Rio de Janeiro/Misc/Qualidade_do_ar_-_Dados_hor%C3%A1rios.csv'

# =============================================================================
# Extract the data            
# =============================================================================


#Open the CSV and count the number of rows
with open(filepath) as csvfile:
    readCSV1 = csv.DictReader(csvfile, delimiter=',')
    firstrow = next(readCSV1, None)
    row_count = sum(1 for rows in readCSV1)


#Go through each row in the csv and extract all of the relevant data
with open(filepath) as csvfile:
    readCSV = csv.DictReader(csvfile, delimiter=',')
    index = 0
    for row in readCSV:
        date = dateutil.parser.parse(row['Data'])
        date = date.date()
        if startdate <= date <= enddate:
            loca = row['Estação']
            for metric in metrics:
                if row[metric] != '':
                    datadict[loca][date][metric].append(float(row[metric]))
                else:
                    datadict[loca][date][metric].append([])
        index+=1
        if index % 10000 == 0:
            print(str(index/row_count*100) + '% Complete')  
    
#Go through each metric and calculate the daily average, then add it to the output dictionary
dayindex = 0
for day in datadict[location].keys():
    for location in locations.keys():
        for metric in metrics:
            metricdata = datadict[location][day][metric]
            denom = sum(1 for z in metricdata if isinstance(z,float))
            if denom > 0:
                value = sum(z for z in metricdata if isinstance(z,float)) / denom
            else:
                value = np.nan
            daydict[location][day][metric] = value
    dayindex+=1
    if dayindex % 100 == 0:
        print(str(dayindex/len(daylist)*10) + '% of days Complete')



# =============================================================================
#  Save data in output csv       
# =============================================================================


filename = './' + 'Concate' + '_DailyAirQuality' +'.csv'
fields = list(daydict[location][day].keys())
fields.append('CODBAIRRO')
with open(filename,'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    dictlist = []
    for location in locations.keys():
        for datekey in daydict[location].keys():
            appenddict = daydict[location][datekey]
            appenddict['CODBAIRRO'] = locations[location]
            dictlist.append(appenddict)
    writer.writerows(dictlist)               