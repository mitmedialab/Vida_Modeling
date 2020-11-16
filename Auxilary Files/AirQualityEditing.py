#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:44:50 2020

@author: jackreid
"""

import csv
import dateutil
from dateutil import rrule
from datetime import datetime, timedelta

# =============================================================================
# %% Generate Monthly Air Quality Averages from the Hourly Data            
# ============================================================================= 

#List of locations and list of metrics
locations = ['CA','AV','SC','SP','IR','BG','CG','PG']
metrics = ['Rain',
            'Pressure',
            'Solar Radiation',
            'Temperature',
            'Relative Humidity',
            'Wind Direction',
            'Wind Speed',
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
            'PM2.5']

#Set up the list of dates
startdate = dateutil.parser.parse('2011/01/01 00:00:01+00')
enddate = dateutil.parser.parse('2020/05/01 00:00:01+00')
monthrange = rrule.rrule(rrule.MONTHLY, dtstart=startdate, until=enddate)
monthlist = []
for month in monthrange:
    monthlist.append([month, month+dateutil.relativedelta.relativedelta(months=+1)])

#Set up a dictionary to hold the data: Location->Date->Metric
datadict = dict()
for location in locations:
    datadict[location] = dict()
    for month in monthlist:
        datadict[location][month[0]] = dict()
        datadict[location][month[0]]['date'] = month[0]
        for metric in metrics:
            datadict[location][month[0]][metric] = []

#Open the CSV and get a count of the number of rows, to be used for progress tracking
with open('./Data/Qualidade_do_ar_-_Dados_hor%C3%A1rios.csv') as csvfile:
    readCSV1 = csv.reader(csvfile, delimiter=',')
    firstrow = next(readCSV1, None)
    row_count = sum(1 for rows in readCSV1)



#Start the Data Processing
monthindex = 0
for entry in monthlist:
    
    #Set up a temporary dictionary to hold the data for a single month: Location->Metric
    tempdict = dict()
    for location in locations:
        tempdict[location] = dict()
        for metric in metrics:
            tempdict[location][metric] = []

    #Identify all data points within the specific month and save that data
    with open('./Data/Qualidade_do_ar_-_Dados_hor%C3%A1rios.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)
        index = 0
        for row in readCSV:
            date = dateutil.parser.parse(row[1])
            if entry[0] <= date <= entry[1]:
                for metriccolumn in metricnumdict.keys():
                    if row[metriccolumn] != '':
                        tempdict[row[3]][metricnumdict[metriccolumn]].append(float(row[metriccolumn]))
                    else:
                        tempdict[row[3]][metricnumdict[metriccolumn]].append([])
            index+=1
            if index % 10000 == 0:
                print(str(index/row_count*100) + '% Complete')     
    
    #Once all the data for a specific month is obtained, average it and store it in the output dictionary
    for keydict in tempdict.keys():
        for metric in tempdict[keydict].keys():
            metricdata = tempdict[keydict][metric]
            denom = sum(1 for z in metricdata if isinstance(z,float))
            if denom > 0:
                value = sum(z for z in metricdata if isinstance(z,float)) / denom
            else:
                value = []
            # print(metric)
            # print(value)
            datadict[keydict][entry[0]][metric] = value
            
    datadict[keydict][entry[0]]['date'] = entry[0]
    monthindex+=1
    print(str(monthindex/len(monthlist)*100) + '% of months Complete')


#Output the monthly averages as a CSV
fields = list(datadict['CA'][entry[0]].keys())

for key in datadict.keys():
    filename = './Data/Output/' + str(key) +'.csv'
    with open(filename,'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        dictlist = []
        for datekey in datadict[key].keys():
            dictlist.append(datadict[key][datekey])
        writer.writerows(dictlist)
        

#Note: At this point, I saved the dictionary as a pckl to avoid having to run this all at once

# =============================================================================
# %% Calculate Mean Anomaly for pre-and-post-COVID          
# ============================================================================= 

'''Mean Anomaly is a metric that compares how the data during some observation period 
differs from that data during some reference period
'''
#Import the monthly averages from the pickle
import pickle

f = open('datadict.pckl', 'rb')
new_data_dict = pickle.load(f)
f.close()

#Define the Reference Period (pre-COVID)
refstart = dateutil.parser.parse('2011/01/01 00:00:01+00')
refend = dateutil.parser.parse('2020/02/15 00:00:01+00')
        
#Set up a dictionary to hold the reference values: Location->Metric
refDict = dict()
for location in locations:
    refDict[location] = dict()
    for metric in metrics:
        refDict[location][metric] = []

#Calculate Reference Values (average value of each metric over the course of the reference period)
for key in new_data_dict.keys():
    tempdict = dict()
    for metric in metrics:
        tempdict[metric] = []
    for datekey in new_data_dict[key].keys():
        if refstart <= datekey <= refend:
            for metric in metrics:
                tempdict[metric].append(new_data_dict[key][datekey][metric])
    for metric in metrics:
        metricdata = tempdict[metric]
        denom = sum(1 for z in metricdata if isinstance(z,float))
        if denom > 0:
            value = sum(z for z in metricdata if isinstance(z,float)) / denom
        else:
            value = []
        refDict[key][metric] = value

#Set up a dictionary to hold the Mean Anomaly values: Location->Metric
anomalyDict = dict()
for location in locations:
    anomalyDict[location] = dict()
    anomalyDict[location]['location'] = location
    for metric in metrics:
        anomalyDict[location][metric] = []

#Calculate Mean Anomaly values (average difference between the post-COVID values and the reference value)
for key in new_data_dict.keys():
    
    #Set up a temporary dictionary to hold a specific locations data
    tempdict = dict()
    for metric in metrics:
        tempdict[metric] = []
    
    #Iterate through each month and calculate the anomaly (the difference between that month's value and the reference value)
    for datekey in new_data_dict[key].keys():
        if refend <= datekey:
            for metric in metrics:
                if refDict[key][metric] != [] and new_data_dict[key][datekey][metric] != []:
                    if type(refDict[key][metric]) is list or type(new_data_dict[key][datekey][metric]) is list:
                        print(refDict[key][metric])
                        print(new_data_dict[key][datekey][metric])
                    anomaly = new_data_dict[key][datekey][metric] - refDict[key][metric]
                else:
                    anomaly = []
                tempdict[metric].append(anomaly)
    
    #Go back over the metrics and calculate the average difference
    for metric in metrics:
        metricdata = tempdict[metric]
        denom = sum(1 for z in metricdata if isinstance(z,float))
        if denom > 0:
            value = sum(z for z in metricdata if isinstance(z,float)) / denom
        else:
            value = []
        anomalyDict[key][metric] = value
        
#Output the Mean Anomaly data as a csv
fields = list(anomalyDict['CA'].keys())
filename = './Data/Output/' + 'MeanAnomaly' +'.csv'
with open(filename,'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    dictlist = []
    for key in anomalyDict.keys():
        dictlist.append(anomalyDict[key])
    writer.writerows(dictlist)
        
    
# =============================================================================
# %% Calculate Daily Averages for the Post-COVID Time Period        
# ============================================================================= 

metrics = ['Rain',
            'Pressure',
            'Solar Radiation',
            'Temperature',
            'Relative Humidity',
            'Wind Direction',
            'Wind Speed',
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
            'PM2.5']

metricnumdict = dict(list(enumerate(metrics,4)))

#Identify dates of interest
startdate = dateutil.parser.parse('2020/03/07 00:00:01+00')
enddate = dateutil.parser.parse('2020/07/01 00:00:01+00')
dayrange = rrule.rrule(rrule.DAILY, dtstart=startdate, until=enddate)
daylist = []
for day in dayrange:
    daylist.append([day, day+dateutil.relativedelta.relativedelta(days=+1)])


#Set up a dictionary to hold the values: Day->Metric
datadict = dict()

for day in daylist:
    datadict[day[0]] = dict()
    datadict[day[0]]['date'] = day[0]
    for metric in metrics:
        datadict[day[0]][metric] = []

#Open the CSV with that I manually cut down to approximately the relevant dates
with open('/home/jackreid/Downloads/temp.csv') as csvfile:
    readCSV1 = csv.reader(csvfile, delimiter=',')
    firstrow = next(readCSV1, None)
    row_count = sum(1 for rows in readCSV1)

#Iterate through each day
dayindex = 0
for entry in daylist:
    
    #Set up a dictionary to hold the values for a particular day
    tempdict = dict()
    for metric in metrics:
        tempdict[metric] = []

    #Go through each row in the csv and extract all of the relevant data
    with open('/home/jackreid/Downloads/temp.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)
        index = 0
        for row in readCSV:
            date = dateutil.parser.parse(row[1])
            if entry[0] <= date <= entry[1]:
                for metriccolumn in metricnumdict.keys():
                    if row[metriccolumn] != '':
                        tempdict[metricnumdict[metriccolumn]].append(float(row[metriccolumn]))
                    else:
                        tempdict[metricnumdict[metriccolumn]].append([])
            index+=1
            if index % 1000 == 0:
                print(str(index/row_count*100) + '% Complete')     
                        
    #Go through each metric and calculate the daily average, then add it to the output dictionary
    for metric in tempdict.keys():
        metricdata = tempdict[metric]
        denom = sum(1 for z in metricdata if isinstance(z,float))
        if denom > 0:
            value = sum(z for z in metricdata if isinstance(z,float)) / denom
        else:
            value = []
        datadict[entry[0]][metric] = value
        
    datadict[entry[0]]['date'] = entry[0]
    dayindex+=1
    print(str(dayindex/len(daylist)*100) + '% of days Complete')


#Output the daily average data as a csv
fields = list(datadict[entry[0]].keys())

filename = './Data/Output/' + 'DailyAirQuality' +'.csv'
with open(filename,'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    dictlist = []
    for datekey in datadict.keys():
        dictlist.append(datadict[datekey])
    writer.writerows(dictlist)