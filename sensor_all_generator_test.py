import serial
from serial import SerialException
import time
import csv
import os
import pandas as pd
import numpy
import subprocess
import datetime as datetime


import serial.tools.list_ports
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

 

import re
import subprocess
import pandas as pd 





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
        os.remove(upload_file)
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


# subprocess.run(["python3", "pushtosql_flow.py"])
# os.remove('sensor_all' + '.csv')
# start_time = datetime.datetime.now()

            




