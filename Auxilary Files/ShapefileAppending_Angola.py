#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:27:55 2021

@author: jackreid
"""

""" Combine Shapefiles"""

# import shapefile
# import pandas as pd


# filepaths = ['/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Angola/Misc/Angola_FinalProducts/Huambo_City.shp',
#              '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Angola/Misc/Angola_FinalProducts/Lobito_Bay.shp',
#              '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Angola/Misc/Angola_FinalProducts/Luanda_Bay.shp',
#              '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Angola/Misc/Angola_FinalProducts/Luanda_City.shp',
#              '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Angola/Misc/Angola_FinalProducts/Luanda_Offshore.shp',
#              '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Angola/Misc/Angola_FinalProducts/ZEE.shp']

# writepath = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Angola/Shapefiles/Combined_NoData.shp'



# names = ['Huambo_City',
#          'Lobito_Bay',
#          'Luanda_Bay',
#          'Luanda_City',
#          'Luanda_Offshore',
#          'ZEE']

# lands = [True,
#          False,
#          False,
#          True,
#          False,
#          True]

# area_codes = [1,
#               2,
#               3,
#               4,
#               5,
#               6]


# # Read in original shapefiles
# r = []
# for filepath in filepaths:
#     r.append(shapefile.Reader(filepath))

# # Create a new shapefile in memory
# w = shapefile.Writer(writepath)


# w.field('NAME', "C")
# w.field('LAND', 'L')
# w.field('AREA_CODE', 'N')


# index = 0
# for shp in r:
#     for shaperec in shp.shapes():
#         w.shape(shaperec)
#         w.record(names[index],lands[index],area_codes[index])
        
#     index += 1

  
# print('WRITE FIELDS ARE')  
# print(w.fields)


# # Close and save the altered shapefile
# w.close()


def ShapefileFormatter(shpfilepath, datapath,fieldname, writepath):
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
    import dateutil
    from dateutil import rrule
    from datetime import datetime, timedelta
    
    #Import and Format the Excel Data
    df = pd.read_excel (datapath,index_col ="NAME") 

    if fieldname[0] == 'Temporal':
        metrics_raw = []
        metrics_format = []
        for dateval in list(df.keys()):
            metrics_raw.append(dateval)
            # format_date = dateutil.parser.parse(dateval)
            format_date = pd.to_datetime(dateval)
            format_date = format_date.date()
            datestring = format_date.strftime('%y%m%d')
            metrics_format.append(fieldname[1] + datestring)


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
        name = entry['NAME']
        print(name)
        # print('LOOKING FOR:', name)
        if (df.index == name).any():
            namerow =  df.loc[name]
            # print('NAMEROW IS:', namerow)
            namevalue = namerow[valname] 
            # print('FOUND: ' + str(name))
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
        for raw, formatted in zip(metrics_raw, metrics_format):
            if index == 0:
                fieldab = formatted
                print('Adding Field: ' + fieldab)
                w.field(fieldab, "N", 10,10)

            appendvalue = dataextract(shaperec.record,raw)
            if appendvalue != 0 and index == 0:
                print(shaperec.record['NAME'])
                print(formatted)
                print(appendvalue)
            shaperec.record.append(appendvalue)
            
        index+=1
#        if shaperec.record['BAIRRO'] == 'Bangu':
#            print(shaperec.record)
        w.shape(shaperec.shape)
        w.record(*shaperec.record)

                    
    print('WRITE FIELDS ARE')  
    print(w.fields)
#    print('READ FIELDS ARE')

    
    # Close and save the altered shapefile
    w.close()
    return shapefile.Reader(writepath)



metrics = ['Temporal', 'NO2C']



shppath = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Luanda/Shapefiles/Combined_Data_1.shp'
datapath = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Luanda/Misc/Adding_NOPerctangeChange.xlsx'
writepath = '/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Luanda/Shapefiles/Combined_Data_2.shp'


ShapefileFormatter(shppath, datapath, metrics, writepath)




