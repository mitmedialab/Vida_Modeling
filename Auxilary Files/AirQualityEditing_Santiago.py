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







# monthindex = 0
# for entry in monthlist:
#     # inner = dict()
#     # for metric in metrics:
#     #     inner[metric] = []
#     tempdict = dict()
#     for location in locations:
#         tempdict[location] = dict()
#         for metric in metrics:
#             tempdict[location][metric] = []

    
#     with open('./Data/Qualidade_do_ar_-_Dados_hor%C3%A1rios.csv') as csvfile:
#         readCSV = csv.reader(csvfile, delimiter=',')
#         next(readCSV, None)
#         index = 0
#         for row in readCSV:
#             date = dateutil.parser.parse(row[1])
#             if entry[0] <= date <= entry[1]:
#                 for metriccolumn in metricnumdict.keys():
#                     if row[metriccolumn] != '':
#                         tempdict[row[3]][metricnumdict[metriccolumn]].append(float(row[metriccolumn]))
#                     else:
#                         tempdict[row[3]][metricnumdict[metriccolumn]].append([])
#             index+=1
#             if index % 10000 == 0:
#                 print(str(index/row_count*100) + '% Complete')     
                        
#     for keydict in tempdict.keys():
#         for metric in tempdict[keydict].keys():
#             metricdata = tempdict[keydict][metric]
#             denom = sum(1 for z in metricdata if isinstance(z,float))
#             if denom > 0:
#                 value = sum(z for z in metricdata if isinstance(z,float)) / denom
#             else:
#                 value = []
#             # print(metric)
#             # print(value)
#             datadict[keydict][entry[0]][metric] = value
#     datadict[keydict][entry[0]]['date'] = entry[0]
#     monthindex+=1
#     print(str(monthindex/len(monthlist)*100) + '% of months Complete')


# fields = list(datadict['CA'][entry[0]].keys())

# for key in datadict.keys():
#     filename = './Data/Output/' + str(key) +'.csv'
#     with open(filename,'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fields)
#         writer.writeheader()
#         dictlist = []
#         for datekey in datadict[key].keys():
#             dictlist.append(datadict[key][datekey])
#         writer.writerows(dictlist)
        

# import pickle

# f = open('datadict.pckl', 'rb')
# new_data_dict = pickle.load(f)
# f.close()



# refstart = dateutil.parser.parse('2011/01/01 00:00:01+00')
# refend = dateutil.parser.parse('2020/02/15 00:00:01+00')
        


# refDict = dict()
# for location in locations:
#     refDict[location] = dict()
#     for metric in metrics:
#         refDict[location][metric] = []

# #Calculate Reference Values
# for key in new_data_dict.keys():
#     tempdict = dict()
#     for metric in metrics:
#         tempdict[metric] = []
#     for datekey in new_data_dict[key].keys():
#         if refstart <= datekey <= refend:
#             for metric in metrics:
#                 tempdict[metric].append(new_data_dict[key][datekey][metric])
#     for metric in metrics:
#         metricdata = tempdict[metric]
#         denom = sum(1 for z in metricdata if isinstance(z,float))
#         if denom > 0:
#             value = sum(z for z in metricdata if isinstance(z,float)) / denom
#         else:
#             value = []
#         refDict[key][metric] = value

# #Calculate Anomaly Values

# anomalyDict = dict()
# for location in locations:
#     anomalyDict[location] = dict()
#     anomalyDict[location]['location'] = location
#     for metric in metrics:
#         anomalyDict[location][metric] = []

# for key in new_data_dict.keys():
#     tempdict = dict()
#     for metric in metrics:
#         tempdict[metric] = []
#     for datekey in new_data_dict[key].keys():
#         if refend <= datekey:
#             for metric in metrics:
#                 if refDict[key][metric] != [] and new_data_dict[key][datekey][metric] != []:
#                     if type(refDict[key][metric]) is list or type(new_data_dict[key][datekey][metric]) is list:
#                         print(refDict[key][metric])
#                         print(new_data_dict[key][datekey][metric])
#                     anomaly = new_data_dict[key][datekey][metric] - refDict[key][metric]
#                 else:
#                     anomaly = []
#                 tempdict[metric].append(anomaly)
#     for metric in metrics:
#         metricdata = tempdict[metric]
#         denom = sum(1 for z in metricdata if isinstance(z,float))
#         if denom > 0:
#             value = sum(z for z in metricdata if isinstance(z,float)) / denom
#         else:
#             value = []
#         anomalyDict[key][metric] = value
        
# fields = list(anomalyDict['CA'].keys())

# filename = './Data/Output/' + 'MeanAnomaly' +'.csv'
# with open(filename,'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fields)
#     writer.writeheader()
#     dictlist = []
#     for key in anomalyDict.keys():
#         dictlist.append(anomalyDict[key])
#     writer.writerows(dictlist)
        
    
    
# metrics = ['Rain',
#             'Pressure',
#             'Solar Radiation',
#             'Temperature',
#             'Relative Humidity',
#             'Wind Direction',
#             'Wind Speed',
#             'SO2',
#             'NO2',
#             'HCNM',
#             'HCT',
#             'CH4',
#             'CO',
#             'NO',
#             'NOx',
#             'O3',
#             'PM10',
#             'PM2.5']

# metricnumdict = dict(list(enumerate(metrics,4)))

# startdate = dateutil.parser.parse('2020/03/07 00:00:01+00')
# enddate = dateutil.parser.parse('2020/07/01 00:00:01+00')
# dayrange = rrule.rrule(rrule.DAILY, dtstart=startdate, until=enddate)
# daylist = []
# for day in dayrange:
#     daylist.append([day, day+dateutil.relativedelta.relativedelta(days=+1)])


    
# datadict = dict()

# for day in daylist:
#     datadict[day[0]] = dict()
#     datadict[day[0]]['date'] = day[0]
#     for metric in metrics:
#         datadict[day[0]][metric] = []


# with open('/home/jackreid/Downloads/temp.csv') as csvfile:
#     readCSV1 = csv.reader(csvfile, delimiter=',')
#     firstrow = next(readCSV1, None)
#     row_count = sum(1 for rows in readCSV1)


# dayindex = 0
# for entry in daylist:
#     tempdict = dict()
#     for metric in metrics:
#         tempdict[metric] = []

    
#     with open('/home/jackreid/Downloads/temp.csv') as csvfile:
#         readCSV = csv.reader(csvfile, delimiter=',')
#         next(readCSV, None)
#         index = 0
#         for row in readCSV:
#             date = dateutil.parser.parse(row[1])
#             if entry[0] <= date <= entry[1]:
#                 for metriccolumn in metricnumdict.keys():
#                     if row[metriccolumn] != '':
#                         tempdict[metricnumdict[metriccolumn]].append(float(row[metriccolumn]))
#                     else:
#                         tempdict[metricnumdict[metriccolumn]].append([])
#             index+=1
#             if index % 1000 == 0:
#                 print(str(index/row_count*100) + '% Complete')     
                        
    
#     for metric in tempdict.keys():
#         metricdata = tempdict[metric]
#         denom = sum(1 for z in metricdata if isinstance(z,float))
#         if denom > 0:
#             value = sum(z for z in metricdata if isinstance(z,float)) / denom
#         else:
#             value = []
#         datadict[entry[0]][metric] = value
#     datadict[entry[0]]['date'] = entry[0]
#     dayindex+=1
#     print(str(dayindex/len(daylist)*100) + '% of days Complete')


# fields = list(datadict[entry[0]].keys())

# filename = './Data/Output/' + 'DailyAirQuality' +'.csv'
# with open(filename,'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fields)
#     writer.writeheader()
#     dictlist = []
#     for datekey in datadict.keys():
#         dictlist.append(datadict[datekey])
#     writer.writerows(dictlist)