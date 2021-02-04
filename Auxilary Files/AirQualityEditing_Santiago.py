#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:44:50 2020

@author: jackreid

Calculates the mean anomaly for various air quality metrics using the 2020 data
"""

import csv
import dateutil
from dateutil import rrule
from datetime import datetime, timedelta


# =============================================================================
#  Define the initial parameters   
# =============================================================================

filepaths = ['./Data/Santiago/Misc/Air Quality/CO-2020_std.csv',
             './Data/Santiago/Misc/Air Quality/MP2.5-2020_std.csv',
             './Data/Santiago/Misc/Air Quality/MP10-2020_std.csv',
             './Data/Santiago/Misc/Air Quality/NO2-2020_std.csv',
             './Data/Santiago/Misc/Air Quality/O3-2020_std.csv',
             './Data/Santiago/Misc/Air Quality/SO2-2020_std.csv']

average_path = './Data/Santiago/Misc/Air Quality/PreCovidAverages.csv'

locations = ['Independencia', 'La_Florida',	'Las_Condes', 'Santiago',
             'Pudahuel', 'Cerrillos', 'El_Bosque', 'Cerro_Navia',
             'Puente_Alto', 'Talagante', 'Quilicura']

metrics = ['CO',
            'MP2.5',
            'MP10',
            'NO2',
            'O3',
            'SO2']



# =============================================================================
#  Calculate mean anomaly for 2020      
# =============================================================================

averagedict = dict()
for metric in metrics:
    averagedict[metric] = dict()

with open(average_path) as csvfile:
    readCSV1 = csv.DictReader(csvfile, delimiter=',')
    j = [0,1,2,3,4,5]
    for each in j:
        firstrow = next(readCSV1, None)

    for row in readCSV1:
        for location in locations:
            averagedict[row['Nombre de estacion']][location] = row[location]

datadict = dict()
for location in locations:
    datadict[location] = dict()
    for metric in metrics:
        datadict[location][metric] = []

places = [0,1,2,3,4,5]
for i in places:
    filepath = filepaths[i]
    metric = metrics[i]
    
    with open(filepath) as csvfile:
        readCSV1 = csv.DictReader(csvfile, delimiter=',')
        j = [0,1,2,3,4,5]
        for each in j:
            firstrow = next(readCSV1, None)
        
        for row in readCSV1:
            for location in locations:
                if row[location] != '' and averagedict[metric][location] != '':
                    anomaly = float(row[location]) - float(averagedict[metric][location])
                    datadict[location][metric].append(anomaly) 

meananomaly = dict()
for location in locations:
    meananomaly[location] = dict()
    for metric in metrics:
        if averagedict[metric][location] != '' and len(datadict[location][metric])>0:
            meananomaly[location][metric] = sum(datadict[location][metric])/len(datadict[location][metric])



