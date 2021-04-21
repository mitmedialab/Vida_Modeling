#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:57:26 2020

@author: jackreid

Based on: https://blackmarble.gsfc.nasa.gov/Tools.html
"""

import gdal, os
import subprocess

hd5Folder = '/home/jackreid/Downloads/indonesia/hd5/'
hd5Folder_space = '/home/jackreid/Downloads/indonesia/hd5/'
tempFolder = '/home/jackreid/Downloads/indonesia/temp/'
tempFolder_space = '/home/jackreid/Downloads/indonesia/temp/'
geotiffFolder = '/home/jackreid/Downloads/indonesia/geotiff/'



# # =============================================================================
# # CONVERT HD5 TO GEOTIFF              
# # =============================================================================

# ## List input raster files
# os.chdir(hd5Folder_space)
# rasterFiles = os.listdir(os.getcwd())

# #Get File Name Prefix
# i = 1
# for file in rasterFiles:
#     # print(rasterFiles)

#     rasterFilePre = file[:-3]
#     print(rasterFilePre)

#     fileExtension = "_BBOX.tif"
    
#     ## Open HDF file
#     hdflayer = gdal.Open(file, gdal.GA_ReadOnly)
    
#     # print (hdflayer.GetSubDatasets())
#     requestedLayers = [4,11]
#     # Open raster layer
#     for layer in hdflayer.GetSubDatasets():
        
#         #hdflayer.GetSubDatasets()[0][0] - for first layer
#         #hdflayer.GetSubDatasets()[1][0] - for second layer ...etc
#         subhdflayer = layer[0]
#         rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)
#         #outputName = rlayer.GetMetadata_Dict()['long_name']
    
#         #Subset the Long Name
#         outputName = subhdflayer[92:]
        
#         outputNameNoSpace = outputName.strip().replace(" ","_").replace("/","_")
#         outputNameFinal = rasterFilePre + outputNameNoSpace + fileExtension
#         # print(outputNameFinal)
    
#         outputFolder = tempFolder_space
        
#         outputRaster = outputFolder + outputNameFinal
        
#         #collect bounding box coordinates
#         HorizontalTileNumber = int(rlayer.GetMetadata_Dict()["HorizontalTileNumber"])
#         VerticalTileNumber = int(rlayer.GetMetadata_Dict()["VerticalTileNumber"])
            
#         WestBoundCoord = (10*HorizontalTileNumber) - 180
#         NorthBoundCoord = 90-(10*VerticalTileNumber)
#         EastBoundCoord = WestBoundCoord + 10
#         SouthBoundCoord = NorthBoundCoord - 10
        
        
#         EPSG = "-a_srs EPSG:4326" #WGS84
        
#         translateOptionText = EPSG+" -a_ullr " + str(WestBoundCoord) + " " + str(NorthBoundCoord) + " " + str(EastBoundCoord) + " " + str(SouthBoundCoord)
        
#         translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine(translateOptionText))
#         gdal.Translate(outputRaster,rlayer, options=translateoptions)
    
#     filepre = rasterFilePre
#     commandtext = 'gdal_merge.py -separate -o ' + geotiffFolder + filepre + '.tif ' + tempFolder + filepre + '*tif'
#     subprocess.call(commandtext, shell=True)
#     subprocess.call('rm ' + tempFolder + filepre + '*tif', shell=True)
        
# # =============================================================================
# #  UPLOAD TO GOOGLE CLOUD STORAGE              
# # =============================================================================
# filenames = subprocess.getoutput('find ' + geotiffFolder + " -name '*.tif'")
# bucket = 'indonesia_nightlights_a2_v1'
# totalLength = len(filenames.split())
# index = 0
# #Iterate through and upload each image
# for file in filenames.split():
#     subprocess.call('gsutil -m cp ' + file + ' gs://' + bucket + '/',
#                     shell=True)
#     index+=1
#     percentageComplete = index/totalLength*100
#     print(str(percentageComplete) + "% Complete")


# =============================================================================
#  IMPORT INTO GEE               
# =============================================================================
  #Import libraries
from xml.dom import minidom
import os
import re
import datetime
filenamelist = subprocess.getoutput('find ' + geotiffFolder + " -name '*.tif'")
bucket = 'indonesia_nightlights_a2_v1'

#Load key word arguments
destination = 'indonesia_nightlights_a2_v1'
user_name = 'jackreid'
metadata_flag = 1
    
#Initiate null list to track asset id names to avoid overwrites
asset_list = []

#Iterate through each filename
index = 0
totalLength = len(filenamelist.split())
for file in filenamelist.split():
# for file in filenamelist.split()[1:2]:
    
    #Identify base name of the file and the date of image to serve as central component of asset id        
    base_name = os.path.basename(os.path.normpath(file))
    folder_filepath = re.sub(base_name, '', file)
    folder_name = os.path.basename(os.path.normpath(folder_filepath))
    sep = '.'
    date_name = base_name.split(sep)[1]
    year = date_name[1:5]
    daynum = date_name[5:8]
    
    prod_name = base_name.split(sep)[4]
    hour = prod_name[7:9]
    minute = prod_name[9:11]
    second = prod_name[11:13]
    fulldate = datetime.datetime(int(year), 1, 1) + datetime.timedelta(int(daynum) - 1)
    day = '{:02d}'.format(fulldate.day)
    month = '{:02d}'.format(fulldate.month)
    
    vdate = year + '-' + month + '-' + day + 'T' + hour + ':' + minute + ':' + second
    #Concatante asset id name
    assetname = base_name[-17:-4]
            
    #Check if asset id already exists, generate number to append if so
    assetflag = 0
    for i in asset_list: 
        if(i == assetname):
            assetflag += 1
    asset_list.append(assetname)
    if assetflag != 0:
        assetname = assetname + '_' + str(assetflag)
    

    timestring = ' --time_start=' + vdate
        
    
    #Generate command sequence for importing the asset
    assetstring = ' --asset_id=users/' + user_name + '/' + destination + '/' + assetname
    bucketstring = ' gs://' + bucket + '/' + base_name
    commandstring = 'earthengine upload image' + assetstring + timestring + bucketstring
    print(commandstring)
    
    #Run the command sequence
    subprocess.call(commandstring,
                    shell=True)
    
    index+=1
    percentageComplete = index/totalLength*100
    print(str(percentageComplete) + "% Complete")
    