#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 13:57:03 2020

@author: jackreid
"""

def ShapefileFormatter(shpfilepath, datapath,fieldname, fieldabr, writepath):
    """Uses pandas to import an Excel matrix as a Dataframe and format it
    to pull out Median Household Income for each county in the US
    
    It then uses the pyshp library (also known as shapefile) to import a shapefile
    containing geometries of each state in the US. 
    
    Finally it saves a new shapefile that is a copy of the imported one, with 
    Median Household Income appended to the record of each county.
    
    [NOTE: CURRENTLY CONFIGURED TO LOOK FOR BAIRRO NAME MATCHES]
    
    Args:
        shpfilepath: file path to the input shapefile
        datapath: file path to the excel spreadsheet with the relevant data.
        fieldname: the column title in the spreadsheet of the data to be added
        fieldabr: the actual title of the field to be added to the shapefile
        writepath: destination and title of the output shapefile
                           
    Returns:
        r2: The output shapefile that was saved to write path.
        """
        
    import pandas as pd
    import shapefile
    
    #Import and Format the Excel Data
    df = pd.read_excel (datapath,index_col ="NAME") 
    # df_range = df.iloc[:,0:20] 
    # df_range[fieldname] = df.loc[:,fieldname]
    
    # Read in original shapefile
    r = shapefile.Reader(shpfilepath)
    
    # Create a new shapefile in memory
    w = shapefile.Writer(writepath)
    
    # Copy over the existing fields
    fields = r.fields
    for name in fields:
        if type(name) == "tuple":
            continue
        else:
            args = name
            w.field(*args)
            

    
    
    #Define a function to identify spreadsheet value based on name
    def dataextract(entry,valname):
        name = entry['BAIRRO']
        # print('LOOKING FOR:', name)
        if (df.index == name).any():
            namerow =  df.loc[name]
            # print('NAMEROW IS:', namerow)
            namevalue = namerow[valname] 
            # print('FOUND: ' + name)
            # print('VALUE IS:', namevalue)
        else:
            namevalue = 0
        if namevalue == '[]':
            namevalue = 0
            # print('NAME NOT FOUND')
            
        return namevalue
    
    
    # Copy over exisiting records and geometries, appending MHI to each record
     
    # Add new field for data
    # newshaperecs = []
    index = 0

    for shaperec in r.iterShapeRecords():
        for metric in fieldname:
            if index == 0:
                fieldab = fieldabr[metric]
                # print('Adding Field: ' + fieldab)
                w.field(fieldab, "N", 10,10)

            appendvalue = dataextract(shaperec.record,metric)
            # if appendvalue != 0:
            #     print(shaperec.record['BAIRRO'])
            #     print(metric)
            #     print(appendvalue)
            shaperec.record.append(appendvalue)
            
        index+=1
        if shaperec.record['BAIRRO'] == 'Bangu':
            print(shaperec.record)
        w.shape(shaperec.shape)
        w.record(*shaperec.record)

                    
    print('WRITE FIELDS ARE')  
    print(w.fields)
    print('READ FIELDS ARE')

    
    # Close and save the altered shapefile
    w.close()
    return shapefile.Reader(writepath)

import pickle

f = open('anomalyMean.pckl', 'rb')
new_data_dict = pickle.load(f)
f.close()

metrics = list(new_data_dict['CA'].keys())
metrics.remove('location')

namedict = {'Rain':'Rain',
 'Pressure':'Pres',
 'Solar Radiation':'SolRad',
 'Temperature':'Temp',
 'Relative Humidity':'Humid',
 'Wind Direction':'WindDir',
 'Wind Speed':'WindSpd',
 'SO2':'SO2',
 'NO2':'NO2',
 'HCNM':'HCNM',
 'HCT':'HCT',
 'CH4':'CH4',
 'CO':'CO',
 'NO':'NO',
 'NOx':'NOx',
 'O3':'O3',
 'PM10':'PM10',
 'PM2.5':'PM2_5'}

shppath = './Data/Shapefiles/Bairros.shp'
datapath = './Data/Output/MeanAnomaly.xlsx'
writepath = './Data/Shapefiles/Bairros_AQ.shp'


ShapefileFormatter(shppath, datapath, metrics, namedict, writepath)



