#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 15:14:50 2020

@author: jackreid
"""

import shapefile
import datetime
import dateutil
from datetime import datetime, timedelta
from dateutil import rrule
import csv

# =============================================================================
# %% Cut the shapefile to queretaro        
# =============================================================================  

# r = shapefile.Reader('./Data/Querétaro/Shapefiles/queretaro_no_data_simplify.shp')

# w = shapefile.Writer('./Data/Mexico/Shapefiles/queretaro_no_data.shp')
 
# # Copy over the existing fields
# fields = r.fields
# for name in fields:
#     if type(name) == "tuple":
#         continue
#     else:
#         args = name
#         w.field(*args)
        
# #Copy over the existing shapes and records
# for shaperec in r.iterShapeRecords():
#     if shaperec.record['ADM1_PCODE'] == 'MX22':
#         shaperec.record['validTo'] = ''
#         w.record(*shaperec.record)
#         w.shape(shaperec.shape)

# # Close and save the altered shapefile
# w.close()

# # =============================================================================
# # %% Cut the coronavirus data to queretaro          
# # =============================================================================  
# filepath = '/home/jackreid/Downloads/temp/201015COVID19MEXICO.csv'
# writepath = '/home/jackreid/Downloads/temp/queretaro_covid_data.csv'

# relevant = []
# with open(filepath,encoding="ISO 8859-1") as csv_file:
#             csvread = csv.DictReader(csv_file)
#             for row in csvread:
#                 if row['ENTIDAD_RES'] == '22' and row["CLASIFICACION_FINAL"] in ['1','2','3']:

#                     relevant.append(row)

# print('DONE READING')

# with open(writepath, mode='w',encoding="ISO 8859-1") as csv_file:
#     fieldnames = list(relevant[0].keys())
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#     writer.writeheader()
#     for row in relevant: 
#         writer.writerow(row)


# # =============================================================================
# # %% Convert case data to cumulative data            
# # =============================================================================  
# muni = dict()
# fields = ['New Cases', 
#               'New Deaths',
#               'New Hospitalizations',
#               'Est. Net Cases',
#               'Est. Net Hospitalizations',
#               'Est. Newly Recovered'
#               ]
# startdate = dateutil.parser.parse('2020/02/10')
# enddate = dateutil.parser.parse('2020/10/30')
# dayrange = rrule.rrule(rrule.DAILY, dtstart=startdate, until=enddate)
# daylist = []
# for day in dayrange:
#     daylist.append([day, day+dateutil.relativedelta.relativedelta(days=+1)])

# # for i in range(1,19):
#     # muni[i] = dict()
    
# for day in daylist:
#     muni[day[0]] = dict()
#     for f in fields:
#         muni[day[0]][f] = 0

# filepath =  '/home/jackreid/Downloads/temp/queretaro_covid_data.csv'

# with open(filepath,encoding="ISO 8859-1") as csv_file:
#             csvread = csv.DictReader(csv_file)
#             for row in csvread:
                
#                 #New Cases
#                 casedate = dateutil.parser.parse(row['FECHA_INGRESO'])
#                 muni[casedate]['New Cases'] += 1
#                 muni[casedate]['Est. Net Cases'] += 1
    
#                 #New Deaths
#                 deathdatestr = row['FECHA_DEF']
#                 if deathdatestr == "9999-99-99":
#                     deathdate = False
#                 else:
#                     deathdate = dateutil.parser.parse(deathdatestr)
#                     muni[deathdate]['New Deaths'] +=1
                    
#                 #Est. Net Cases & Est. Newly Recovered
#                 if deathdate:
#                     muni[deathdate]['Est. Net Cases'] -= 1
#                 else:
#                     recovdate = casedate + dateutil.relativedelta.relativedelta(days=+14)
#                     muni[recovdate]['Est. Newly Recovered'] += 1
#                     muni[recovdate]['Est. Net Cases'] -= 1
                    
#                 #New Hospitalizations
#                 if row['TIPO_PACIENTE'] == '2':
#                     muni[casedate]['New Hospitalizations'] += 1
#                     muni[casedate]['Est. Net Hospitalizations'] += 1
#                     if deathdate:
#                         muni[deathdate]['Est. Net Hospitalizations'] -= 1
#                     else:
#                         muni[recovdate]['Est. Net Hospitalizations'] -= 1
                        

        
# writepath = '/home/jackreid/Downloads/temp/queretaro_covid_data_processed.csv'

# with open(writepath, mode='w',encoding="ISO 8859-1") as csv_file:
#     fieldnames = ['Date'] + fields
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#     writer.writeheader()
#     for day in muni.keys():
#         writedic = dict()
#         writedic['Date'] = day
#         for f in fields:
#             writedic[f] = muni[day][f]
            
#         writer.writerow(writedic)


# =============================================================================
# %% Get cumulative values for each municipalit            
# =============================================================================  





fields = ['Cumulative Cases', 
              'Cumulative Deaths',
              'Cumulative Hospitalizations'
              ]


muni = dict()
for i in range(1,19):
    muni[i] = dict()
    for f in fields:
        muni[i][f] = 0
    

filepath =  '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Querétaro/Misc/queretaro_covid_data.csv'

with open(filepath,encoding="ISO 8859-1") as csv_file:
            csvread = csv.DictReader(csv_file)
            for row in csvread:
                
                #New Cases
                location = int(row['MUNICIPIO_RES'])
                muni[location]['Cumulative Cases'] += 1
    
                #New Deaths
                deathdatestr = row['FECHA_DEF']
                if deathdatestr == "9999-99-99":
                    deathdate = False
                else:
                    muni[location]['Cumulative Deaths'] +=1
                    
                    
                #New Hospitalizations
                if row['TIPO_PACIENTE'] == '2':
                    muni[location]['Cumulative Hospitalizations'] += 1

        
writepath = '/home/jackreid/Downloads/temp/queretaro_cumulative.csv'

with open(writepath, mode='w',encoding="ISO 8859-1") as csv_file:
    fieldnames = ['Municipality'] + fields
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for municipality in muni.keys():
        writedic = dict()
        writedic['Municipality'] = municipality
        for f in fields:
            writedic[f] = muni[municipality][f]
            
        writer.writerow(writedic)







