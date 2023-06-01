# -*- coding: utf-8 -*-
"""
Created on Tue May 23 21:17:44 2023

@author: willk
"""

import pandas as pd
import os
from datetime import date

def define_path(mySource):
    myLaptop = "TBD"
    myDesktop = "C:/Users/willk/OneDrive/Desktop/GitHub/stocks_project_files/"
    if mySource == "desktop":
        return myDesktop
    else:
        return myLaptop

def get_file_names(myType, myDf, mySource, myStart, myEnd):
    myPath = mySource
    dir_list = os.listdir(myPath + myType)
    
    for item in dir_list:
        if item[0].lower() >= myStart.lower() and item[0].lower() <= myEnd.lower():
            myDf.loc[len(myDf.index)] = [myType, item] 
    return myDf

def build_master(myPath, myLookup, myStart, myEnd):
    myMaster = pd.DataFrame(columns=['Symbol', 'Type', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    myLookup = myLookup.reset_index()
    
    for index, row in myLookup.iterrows():
        print("Fetching (" + str(index) + "/" + str(len(myLookup.index) - 1) + ") " + row['Filename'] + " data")
        myFilePath = myPath+"/"+row['Type']+"/"+row['Filename']
        fileDf = pd.read_csv(myFilePath)
        fileDf['Date'] = pd.to_datetime(fileDf['Date'])
        
        temp = (fileDf['Date'] >= myStart) & (fileDf['Date'] <= myEnd)
        fileDf = fileDf.loc[temp]
        fileDf.insert(loc = 0,
                      column = "Symbol",
                      value = row['Symbol'])
        fileDf.insert(loc = 1,
                      column = "Type",
                      value = row['Type'])
        myMaster = pd.concat([myMaster,fileDf], axis="rows")
        
    myMaster = myMaster.reset_index(drop=True)
    return myMaster

def file_stats(myPath, myLookup, myStart, myEnd):
    myMaster = pd.DataFrame(columns=['Symbol', 'Type', 'Size'])
    myLookup = myLookup.reset_index(drop = True)
    
    for index, row in myLookup.iterrows():
        print("Fetching (" + str(index) + "/" + str(len(myLookup.index) - 1) + ") " + row['Filename'] + " data")
        myFilePath = myPath+"/"+row['Type']+"/"+row['Filename']
        
        myStats = os.stat(myFilePath)
        
        fileDf = pd.read_csv(myFilePath)
        fileDf['Date'] = pd.to_datetime(fileDf['Date'])
        
        myMaster.loc[len(myMaster.index)] = [row['Symbol'], row['Type'], (myStats.st_size / (1024 * 1024))]
        
    myMaster = myMaster.reset_index(drop=True)
    return myMaster

# define variables
source = "desktop"
startLetter = "a"
endLetter = "z"
startDate = "2015-01-01"
endDate = "2020-12-31"

# build path and blank dfs
absolutePath = define_path(source)
stockFiles = pd.DataFrame(columns=['Type', 'Filename'])
etfFiles = pd.DataFrame(columns=['Type', 'Filename'])
lookupFile = pd.DataFrame(columns=['Type', 'Filename'])

# extract file names
print("Get stock names")
stockFiles = get_file_names("stocks", stockFiles, absolutePath, startLetter, endLetter)
print("Get etf names")
etfFiles = get_file_names("etfs", etfFiles, absolutePath, startLetter, endLetter)

# merge stock and etf dfs into master df
print("Merge stock and etf tables")
lookupFile = pd.concat([stockFiles,etfFiles], axis="rows")
lookupFile['Symbol'] = lookupFile.Filename.str.split(".").str[0]

"""
# get file size stats
fileStats = file_stats(absolutePath, lookupFile, startDate, endDate)
print(fileStats)
fileStats.to_csv(absolutePath + "file_size_" + str(date.today()) + ".csv")

"""
# read through individual fields to extract data
print("Build masterFile")
masterFile = build_master(absolutePath, lookupFile, startDate, endDate)

#export to csv
exportName = absolutePath + "output_" + str(date.today()) + ".csv"
masterFile.to_csv(exportName)

print(masterFile)
print(exportName)
