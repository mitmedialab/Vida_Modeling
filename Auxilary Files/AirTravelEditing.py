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

locations = ['Arica y Parinacota',
             'Biobío',
             'Coquimbo',
             'Metropolitana',
             'Los Lagos',
             'Araucanía',
             'Antofagasta',
             'Tarapacá',
             'Atacama',
             'Magallanes',
             'Aysén',
             'Los Ríos',
             'Valparaíso']

metrics = ['Operaciones',
            'Pasajeros']

#metricnumdict = dict(list(enumerate(metrics,4)))

startdate = dateutil.parser.parse('2019/12/31')
enddate = dateutil.parser.parse('2020/07/25')
monthrange = rrule.rrule(rrule.WEEKLY, dtstart=startdate, until=enddate)
monthlist = []
for month in monthrange:
    monthlist.append([month, month+dateutil.relativedelta.relativedelta(weeks=+1)])

    
datadict = dict()
for location in locations:
    datadict[location] = dict()
    for month in monthlist:
        datadict[location][month[0]] = dict()
        datadict[location][month[0]]['date'] = month[0]
        for metric in metrics:
            datadict[location][month[0]][metric] = []


with open('./Data/Chile/Misc/TransporteAereo_std.csv') as csvfile:
    readCSV1 = csv.reader(csvfile, delimiter=',')
    firstrow = next(readCSV1, None)
    row_count = sum(1 for rows in readCSV1)




monthindex = 0
for entry in monthlist:
     # inner = dict()
     # for metric in metrics:
     #     inner[metric] = []
     tempdict = dict()
     for location in locations:
         tempdict[location] = dict()
         for metric in metrics:
             tempdict[location][metric] = []


     with open('./Data/Chile/Misc/TransporteAereo_std.csv') as csvfile:
         csvread = csv.DictReader(csvfile)
#         next(readCSV, None)
         index = 0
         for row in csvread:
             date = dateutil.parser.parse(row['Inicio_semana'])
             if entry[0] <= date <= entry[1]:
                 for metric in metrics:
                     if row[metric] != '':
                         tempdict[row['Region_destino']][metric].append(float(row[metric]))
                     else:
                         tempdict[row['Region_destino']][metric].append([])
             index+=1
             if index % 100 == 0:
                 print(str(index/row_count*100) + '% Complete')     
                        
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

#
# fields = list(datadict['CA'][entry[0]].keys())
#
# for key in datadict.keys():
#     filename = './Data/Output/' + str(key) +'.csv'
#     with open(filename,'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fields)
#         writer.writeheader()
#         dictlist = []
#         for datekey in datadict[key].keys():
#             dictlist.append(datadict[key][datekey])
#         writer.writerows(dictlist)
#        

#import pickle

#f = open('datadict.pckl', 'rb')
#new_data_dict = pickle.load(f)
#f.close()



refstart = dateutil.parser.parse('2012/12/31')
refend = dateutil.parser.parse('2020/02/29')
        


refDict = dict()
for location in locations:
    refDict[location] = dict()
    for metric in metrics:
        refDict[location][metric] = []

#Calculate Reference Values
for key in datadict.keys():
    tempdict = dict()
    for metric in metrics:
        tempdict[metric] = []
    for datekey in datadict[key].keys():
        if refstart <= datekey <= refend:
            for metric in metrics:
                tempdict[metric].append(datadict[key][datekey][metric])
    for metric in metrics:
        metricdata = tempdict[metric]
        denom = sum(1 for z in metricdata if isinstance(z,float))
        if denom > 0:
            value = sum(z for z in metricdata if isinstance(z,float)) / denom
        else:
            value = []
        refDict[key][metric] = value

#Calculate Anomaly Values

anomalyDict = dict()
for location in locations:
    anomalyDict[location] = dict()
    anomalyDict[location]['location'] = location
    for metric in metrics:
        anomalyDict[location][metric] = []

for key in datadict.keys():
    tempdict = dict()
    for metric in metrics:
        tempdict[metric] = []
    for datekey in datadict[key].keys():
        if refend <= datekey:
            for metric in metrics:
                if refDict[key][metric] != [] and datadict[key][datekey][metric] != []:
                    if type(refDict[key][metric]) is list or type(datadict[key][datekey][metric]) is list:
                        print(refDict[key][metric])
                        print(datadict[key][datekey][metric])
                    anomaly = datadict[key][datekey][metric] - refDict[key][metric]
                else:
                    anomaly = []
                tempdict[metric].append(anomaly)
    for metric in metrics:
        metricdata = tempdict[metric]
        denom = sum(1 for z in metricdata if isinstance(z,float))
        if denom > 0:
            value = sum(z for z in metricdata if isinstance(z,float)) / denom
        else:
            value = []
        anomalyDict[key][metric] = value
        
fields = list(anomalyDict['Biobío'].keys())

filename = './Data/Chile/Misc/' + 'MeanAnomaly' +'.csv'
with open(filename,'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    dictlist = []
    for key in anomalyDict.keys():
        dictlist.append(anomalyDict[key])
    writer.writerows(dictlist)
        
    
    