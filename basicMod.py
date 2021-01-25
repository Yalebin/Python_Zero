from collections import Counter
import datetime as dt
import numpy as np
import os
import pandas as pd
import re

#讀取指定路徑CSV檔
def readStaData(fileName, fileDir=None):
    if fileDir is None:
        filePath = ''.join([os.getcwd(), "\\", fileName])
    else:
        filePath = ''.join([fileDir, "\\", fileName])
    return pd.read_csv(filePath, dtype=str, encoding='big5')

#檢視DataFrame
def showDfInfo(sourceDf, uniKey=None):
    """
    function: 
        show dataframe and columns info.
    parameter:
        sourceDf_要顯示的Dataframe
        uniKey_具唯一值之鍵值欄位
    return:
        dataframe info.
    """
    if not uniKey is None:
        print('Data row count:', len(sourceDf), 
              'Case count:', len(sourceDf[uniKey].unique()))
    else: 
        print('Data row count:', len(sourceDf))
    #
    print('Total columns:\n', sourceDf.columns.to_list())
    display(sourceDf.head(2))
    
#清除欄位名稱/Index名稱空白鍵
def cleanSignal(dfData, axis=0, columns=None):
    if axis==0: #clean column-names
        colList = dfData.columns.to_list()
        for x in range(0, len(colList)):
            #colList[x] = re.sub(r'[^\w]', '', colList[x])
            colList[x] = colList[x].rstrip()
            dfData.columns = colList
    #
    elif axis==1: #clean every-cell in specific column
        if columns is None:
            return print("Error!!Parameter_columns is None.")
        else:
            for y in columns:
                jobSeries = dfData[y]
                for sIndex, sValue in jobSeries.items():
                    jobSeries[sIndex] = jobSeries[sIndex].rstrip()
                dfData[y] = jobSeries