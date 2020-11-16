#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 20:59:15 2020

@author: jackreid
"""


import csv
import dateutil
from dateutil import rrule
from datetime import datetime, timedelta

# =============================================================================
# %% Calculate Daily Averages for the Post-COVID Time Period        
# ============================================================================= 

codigosnums = [13502,
           13402,
           13403,
           13102,
           13103,
           13301,
           13104,
           13503,
           13105,
           13602,
           13106,
           13107,
           13108,
           13603,
           13109,
           13110,
           13111,
           13112,
           13113,
           13302,
           13114,
           13115,
           13116,
           13117,
           13118,
           13119,
           13504,
           13501,
           13604,
           13404,
           13121,
           13605,
           13122,
           13202,
           13123,
           13124,
           13201,
           13125,
           13126,
           13127,
           13128,
           13401,
           13129,
           13203,
           13130,
           13505,
           13131,
           13101,
           13601,
           13303,
           13132,
           13120]

codigos=[]
for code in codigosnums:
    codigos.append(str(code))



#Identify dates of interest
startdate = dateutil.parser.parse('2020/02/26 00:00:01+00')
startdate = startdate.date()
enddate = dateutil.parser.parse('2020/09/21 00:00:01+00')
enddate = enddate.date()
dayrange = rrule.rrule(rrule.DAILY, dtstart=startdate, until=enddate)
daylist = []
for day in dayrange:
    daylist.append([day, day+dateutil.relativedelta.relativedelta(days=+1)])
weekrange = rrule.rrule(rrule.WEEKLY, dtstart=startdate, until=enddate)
weeklist = []
for week in weekrange:
    weeklist.append([week, week+dateutil.relativedelta.relativedelta(days=+6)])


#Set up a dictionary to hold the values: Day->Metric
datadict = dict()

for day in daylist:
    datadict[day[0].date()] = dict()
    datadict[day[0].date()]['date'] = day[0].date()
    for code in codigos:
        datadict[day[0].date()][code] = []
        


#Open the CSV with that I manually cut down to approximately the relevant dates
with open('/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Santiago/Misc/IndiceDeMovilidad-IM_T.csv') as csvfile:
    readCSV1 = csv.DictReader(csvfile, delimiter=',')
    firstrow = next(readCSV1, None)
    row_count = sum(1 for rows in readCSV1)


#Go through each row in the csv and extract all of the relevant data
with open('/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Santiago/Misc/IndiceDeMovilidad-IM_T.csv') as csvfile:
    readCSV = csv.DictReader(csvfile, delimiter=',')
    index = 0
    for row in readCSV:
        date = dateutil.parser.parse(row['Date'])
        date = date.date()
        if startdate <= date <= enddate:
            for code in codigos:
                if row[code] != '':
                    datadict[date][code] = float(row[code])
                else:
                    datadict[date][code] = []
        index+=1
        if index % 1000 == 0:
            print(str(index/row_count*100) + '% Complete')  
            
            
weekdict = dict()

for week in weeklist:
    weekdict[week[0].date()] = dict()
    weekdict[week[0].date()]['date'] = week[0].date()
    for code in codigos:
        weekdict[week[0].date()][code] = []
        
weekavg = weekdict.copy()
                
        
for day in datadict.keys():
    for week in weeklist:
        # startweek = week[0].date()
        # endweek
        if week[0].date() <= day <= week[1].date():
            for code in codigos:
                weekdict[week[0].date()][code].append(datadict[day][code])

for week in weekdict.keys():
    for code in codigos:
        metricdata = weekdict[week][code]
        # print(metricdata)
        denom = sum(1 for z in metricdata if isinstance(z,float))
        if denom > 0:
            value = sum(z for z in metricdata if isinstance(z,float)) / denom
        else:
            value = []
        weekavg[week][code] = value
    

fields = weekavg[startdate].keys()
filename = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Santiago/Misc/WeeklyMobility.csv'
with open(filename,'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    dictlist = []
    for key in weekavg.keys():
        dictlist.append(weekavg[key])
    writer.writerows(dictlist)
    
# # =============================================================================
# # %% Calculate Mean Anomaly for pre-and-post-COVID          
# # ============================================================================= 


# #Define the Reference Period (pre-COVID)
# refstart = dateutil.parser.parse('2020/02/26 00:00:01+00')
# refstart = refstart.date()
# refend = dateutil.parser.parse('2020/03/02 00:00:01+00')
# refend = refend.date()
        
# #Set up a dictionary to hold the reference values: Location->Metric
# refDict = dict()
# for code in codigos:
#     refDict[code] = []

# #Calculate Reference Values (average value of each code over the course of the reference period)
# tempdict = dict()
# for code in codigos:
#     tempdict[code] = []
    
# for datekey in datadict.keys():
#     if refstart <= datekey <= refend:
#         # print('success')
#         for code in codigos:
#             tempdict[code].append(datadict[datekey][code])
            

# for code in codigos:
#     metricdata = tempdict[code]
#     # print(metricdata)
#     denom = sum(1 for z in metricdata if isinstance(z,float))
#     if denom > 0:
#         value = sum(z for z in metricdata if isinstance(z,float)) / denom
#     else:
#         value = []
#     refDict[code] = value

# #Set up a dictionary to hold the Mean Anomaly values: Location->Metric
# anomalyDict = dict()
# for code in codigos:
#     anomalyDict[code] = []

# #Calculate Mean Anomaly values (average difference between the post-COVID values and the reference value)
    
# #Set up a temporary dictionary to hold a specific locations data
# tempdict = dict()
# for code in codigos:
#     tempdict[code] = []

# #Iterate through each month and calculate the anomaly (the difference between that month's value and the reference value)
# for datekey in datadict.keys():
#     if refend <= datekey:
#         for code in codigos:
#             if refDict[code] != [] and datadict[datekey][code] != []:
#                 # if type(refDict[code]) is list or type(datadict[datekey][code]) is list:
#                     # print(refDict[code])
#                     # print(new_data_dict[datekey][code])
#                 anomaly = datadict[datekey][code] - refDict[code]
#             else:
#                 anomaly = []
#             tempdict[code].append(anomaly)

# #Go back over the codes and calculate the average difference
# for code in codigos:
#     codedata = tempdict[code]
#     denom = sum(1 for z in codedata if isinstance(z,float))
#     if denom > 0:
#         value = sum(z for z in codedata if isinstance(z,float)) / denom
#     else:
#         value = []
#     anomalyDict[code] = value
        
# #Output the Mean Anomaly data as a csv
# fields = datadict[startdate].keys()
# filename = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Santiago/Misc/MobilityMeanAnomaly.csv'
# with open(filename,'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fields)
#     writer.writeheader()
#     dictlist = []
#     for key in anomalyDict.keys():
#         dictlist.append({key:anomalyDict[key]})
#     writer.writerows([anomalyDict])