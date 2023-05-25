# -*- coding: utf-8 -*-
"""
Created on Tue May 23 21:17:44 2023

@author: willk
"""

import pandas as pd
import os

def get_file_names(myType, myDf):
    myPath = "C:/Users/willk/OneDrive/Desktop/GitHub/stocks_project_files/"
    dir_list = os.listdir(myPath + myType)
    
    for item in dir_list:
        myDf.loc[len(myDf.index)] = [myType, item] 
    
    return myDf


stockFiles = pd.DataFrame(columns=['type', 'filename'])
etfFiles = pd.DataFrame(columns=['type', 'filename'])

stockFiles = get_file_names("stocks", stockFiles)
etfFiles = get_file_names("etfs", etfFiles)

print(stockFiles)