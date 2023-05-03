#!/usr/bin/env python
# coding: utf-8

import sqlite3
from google.cloud import storage
import pandas as pd 
import numpy as np
from datetime import datetime
import mysql.connector 
from serial import SerialException
import time
import csv
import os
import datetime as datetime
import serial.tools.list_ports
import re




def replace_string_with_zero(value):
    if isinstance(value, str):
        return 0
    else:
        return value

def replace_negative_with_zero(value):
    if value < 0:
        return abs(0)
    else:
        return value







data_gas = pd.DataFrame()
data_tank = pd.DataFrame()
upload_file_list = ['Sensor_A.csv', 'Sensor_B.csv', 'Sensor_C.csv','Sensor_D.csv', 'Sensor_E.csv']

colnames = ['datetime','vals']
for upload_file in upload_file_list:
    df = pd.read_csv(upload_file,index_col=0, skiprows=0, names = colnames)
    df = df['vals'].str.split(',', expand=True)
    df.index = pd.to_datetime(df.index, format="%a %b %d %X %Y")
    if len(df.columns) > 4:

        df = df.iloc[:, : 5]
        data_gas = data_gas.append(df)
        print(upload_file)
        
    # print(data_gas)
#  else:
#     df = df.iloc[:, : 3]
#     # print('processing tank data')
#     data_tank = data_tank.append(df)
#     os.remove(upload_file)
#     # print(data_tank)
    
    
    
            


#              data[['ID','CH4','CO2','OH','Cnt']]= data.loc[:,'vals'].str.split(',',4, expand =True)
data_gas.columns =['ID','CH4','CO2','OH','Cnt']
data_gas.reset_index(inplace =True)
data_gas.set_index(['datetime'], inplace = True)
#  data_gas = data_gas[::200]
#  data_tank = data_tank[::50]
#              data_tank.columns =['Sensor_value','EQ_waste_height_mm','EQ_volume_%']
try:
    data_tank.columns =['Sensor_value','EQ_waste_height_mm','EQ_volume_%']
except ValueError:
    pass

curr = time.time()
curr = time.ctime(curr) 
uploadfile1 = 'sensor_all' + '.csv'
uploadfile2 = 'tank_data' + '.csv'
data_gas.to_csv(uploadfile1)
data_tank.to_csv(uploadfile2)



            








data = pd.read_csv ('sensor_all.csv')
#data = pd.read_csv (r'/home/farscopestudent/Documents/WASE/wase-cabinet/flowmeter_push.csv')  
df_biogasflow = pd.DataFrame(data)






df_biogasflow['datetime'] = pd.to_datetime(df_biogasflow['datetime'])
df_biogasflow = df_biogasflow[df_biogasflow['ID'].isin([1, 2, 3, 4])]


df_biogasflow.set_index(['datetime', 'ID'], inplace=True)




df_biogasflow = df_biogasflow.applymap(replace_string_with_zero)

df_biogasflow = df_biogasflow.applymap(replace_negative_with_zero)





df_biogasflow = df_biogasflow.groupby(level='ID').resample('30T', level=0).max()











print(df_biogasflow)
df_biogasflow.reset_index(inplace=True)
# df_biogasflow['datetime'] = df_biogasflow['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')









cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='saniWASE_datasets')


 

cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in df_biogasflow.columns.tolist()])
for i,row in df_biogasflow.iterrows():
    sql = "INSERT INTO `gascomp_flowmeter` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

# os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')


cnx.close()

print('pushed')

os.remove('Sensor_A.csv')
os.remove('Sensor_B.csv')
os.remove('Sensor_C.csv')
os.remove('Sensor_D.csv')


