from collections import Counter
import datetime as dt
import numpy as np
import os
import pandas as pd
import re

#轉換指定欄位為Datatime-type
def con2Dt(dfData, colName):
    dfData[colName] = pd.to_datetime(dfData[colName])
    return dfData

#轉置原始Dataframe，並整併日期與時間
def transDatas(dfData, staCol, dayCol, itemCol):
    staName = dfData[staCol].unique()
    staDays = dfData[dayCol].unique()
    staItems = list(dfData[itemCol].unique())
    #transfor item-value to columns, and merge date+hours
    newCols = ['Station', 'Datatime']
    newCols.extend(staItems)
    dfStations = pd.DataFrame(columns=newCols)
    for x in staDays:
        dfTemp = dfData[dfData[dayCol]==x]
        hourList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 
                    '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        tempCols = list(dfTemp[itemCol].unique()) #items's list for specific day
        dfTrans = dfTemp.loc[:, hourList].T
        dfTrans.columns = tempCols
        dfTrans['Station'] = staName[0]
        #
        for s in dfTrans.index:
            dfTrans.loc[s, 'Datatime'] = pd.to_datetime(x)+dt.timedelta(hours=int(s))
            dfStations = dfStations.append(dict(dfTrans.loc[s]), ignore_index=True)
    return dfStations
#驗證與轉置無效值
def verifyValue(dfData, itemList):
    for x in dfData.index:
        for y in dfData.columns.to_list():
            if y in itemList:
                tempFloat = dfData.loc[x, y]
                if ('#' in tempFloat or '*' in tempFloat or 'x' in tempFloat or 'A' in tempFloat):
                    dfData.loc[x, y] = np.nan
                else:
                    try:
                        dfData.loc[x, y] = float(tempFloat)
                    except:
                        continue
