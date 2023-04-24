#!/usr/bin/env python
# coding: utf-8

import sqlite3
from google.cloud import storage
import pandas as pd 
import numpy as np
from datetime import datetime
import mysql.connector 
import sys 
import os
import pandas as pd






data = pd.read_csv ('sensor_all.csv')
#data = pd.read_csv (r'/home/farscopestudent/Documents/WASE/wase-cabinet/flowmeter_push.csv')  
df_biogasflow = pd.DataFrame(data)
print(df_biogasflow)





# def resample_mean(df, time, cols, round_val, level_name):
#   df.dropna(inplace=True)
#   df =  df[(df.astype(float) >= 0.0).all(1)]
#   df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].mean() 
#   df = df.round(round_val)
#   return df

# def resample_sum(df, time, cols, round_val, level_name):
#   df.dropna(inplace=True)
#   df= df[(df.astype(float) >= 0.0).all(1)]
#   df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].sum()
#   df = df.round(round_val)
#   return df

# def resample_max(df, time, cols, round_val, level_name):
#   df.dropna(inplace=True)
#   df= df[(df.astype(float) >= 0.0).all(1)]
#   df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].max()
#   df = df.round(round_val)
#   return df



















cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='saniWASE_datasets')


 

cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in df_biogasflow.columns.tolist()])
for i,row in df_biogasflow.iterrows():
    sql = "INSERT INTO `gascomp_flowmeter` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

# os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')


cnx.close()


