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






df_biogasflow['datetime'] = pd.to_datetime(df_biogasflow['datetime'])



df_biogasflow.set_index(['datetime', 'ID'], inplace=True)

df_biogasflow = df_biogasflow.where(df_biogasflow >= 0, 0)



df_biogasflow = df_biogasflow.groupby(level='ID').resample('10T', level=0).max()











print(df_biogasflow)
df_biogasflow.reset_index(inplace=True)
df_biogasflow['datetime'] = df_biogasflow['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')








cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='saniWASE_datasets')


 

cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in df_biogasflow.columns.tolist()])
for i,row in df_biogasflow.iterrows():
    sql = "INSERT INTO `gascomp_flowmeter` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

# os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')


cnx.close()


