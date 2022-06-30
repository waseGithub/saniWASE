import serial
import time
import csv
import os
import pandas as pd
import numpy


import serial.tools.list_ports
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


#time.sleep(40)
gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  

import re
import subprocess
import pandas as pd 
import dictpy
device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb")
devices = []

line1 = None
line2 = None
line3 = None 
line4 = None 
line5 = None




     
       


ports = serial.tools.list_ports.comports(include_links =False)
ls = []
for port in ports:
    print(port.device)
    ls.append(port.device)
   
print(ls)


import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

Megas = []
unos = []
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        if '7583435393035160F0C1' in hwid:
          print('Requested device found mega 1')
          print(port)
          Megas.append(port)
        elif '5583931353835151B072' in hwid:
          print('Requested device found mega 2')
          print(port)
          Megas.append(port)
        elif '8503731383535161A180' in hwid:
          print('Requested device found mega 3')
          print(port)
          Megas.append(port)
        elif '5503731333735150D090' in hwid:
          print('Requested device found mega 4')
          print(port)
          Megas.append(port)
        elif '758343539303514031D2' in hwid:
          print('Requested device found uno 1')
          print(port)
          unos.append(port)
          
print('Megas as port:')          
print(Megas)
print('Unos as port:')          
print(unos)
         
           

ser1 = serial.Serial(str(ls[0]),  38400, timeout = 25)
ser2 = serial.Serial(str(ls[1]),  38400, timeout = 25)
ser3 = serial.Serial(str(ls[2]),  38400, timeout = 25)
ser4 = serial.Serial(str(ls[4]),  38400, timeout = 25)
ser5 = serial.Serial(str(ls[3]),  38400, timeout = 25)
print("channels correct")
    
time.sleep(5)

if __name__ == '__main__':
    
   
   
    
   
    
    ser1.flush()
    ser2.flush()
    ser3.flush()
    ser4.flush()
    ser5.flush()
    i = 0

   
    while True:
         i +=1
         print('Current count =')
         print(i)
    
       
        
         if ser1.in_waiting > 0:
           
             line1 = ser1.readline().decode("utf-8")
            
            
             with open ("Sensor_A.csv","a") as f:
                
                 writer = csv.writer(f, delimiter=",")
                 writer.writerow([time.asctime(),line1])
                

         if ser2.in_waiting > 0:
           
             line2 = ser2.readline().decode("utf-8")
            
            
             with open ("Sensor_B.csv","a") as f:
                
                 writer = csv.writer(f, delimiter=",")
                 writer.writerow([time.asctime(),line2])
                
                
                
         if ser3.in_waiting > 0:
           
            line3 = ser3.readline().decode("utf-8")
           
            
            with open ("Sensor_C.csv","a") as f:
                
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.asctime(),line3])
         
                
         if ser4.in_waiting > 0:
           
            line4 = ser4.readline().decode("utf-8")
         
            
            with open ("Sensor_D.csv","a") as f:
                
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.asctime(),line4])
          
         if ser5.in_waiting > 0:
           
            line5 = ser5.readline().decode("utf-8")
           
            
            with open ("Sensor_E.csv","a") as f:
                
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.asctime(),line5])
         print('writing gas data')
         print(line1)
         print(line2)
         print(line3)
         print(line4)
         print('writing tank data')
         print(line5)
                
         #######################################
        #######################################
        #change the i value below dependig
        #on how regular updtaes to drive are required  
       #######################################
      #######################################   
                
         if i == 1000: 
             i = 0
             data_gas = pd.DataFrame()
             data_tank = pd.DataFrame()
             upload_file_list = ['Sensor_A.csv', 'Sensor_B.csv', 'Sensor_C.csv','Sensor_D.csv', 'Sensor_E.csv']
             
             colnames = ['datetime','vals']
             for upload_file in upload_file_list:
                 df = pd.read_csv(upload_file,index_col=0, skiprows=5, names = colnames)
                 df = df['vals'].str.split(',', expand=True)
                 df.index = pd.to_datetime(df.index, format="%a %b %d %X %Y")
                 if len(df.columns) > 4:
                    print('processing gas data')
                    df = df.iloc[:, : 5]
                    data_gas = data_gas.append(df)
                    os.remove(upload_file)
                    print(data_gas)
                 else:
                    df = df.iloc[:, : 3]
                    print('processing tank data')
                    data_tank = data_tank.append(df)
                    os.remove(upload_file)
                    print(data_tank)
                    
                    
                  
                         
             
             
#              data[['ID','CH4','CO2','OH','Cnt']]= data.loc[:,'vals'].str.split(',',4, expand =True)
             data_gas.columns =['ID','CH4','CO2','OH','Cnt']
             data_gas.reset_index(inplace =True)
             data_gas.set_index(['datetime'], inplace = True)
             data_gas = data_gas[::200]
             data_tank = data_tank[::200]
             data_tank.columns =['Sensor_value','EQ_waste_height_mm','EQ_volume_%']
             curr = time.time()
             curr = time.ctime(curr) 
             uploadfile1 = 'sensor_all_' + str(curr) + '.csv'
             uploadfile2 = 'tank_data' + str(curr) + '.csv'
             data_gas.to_csv(uploadfile1)
             data_tank.to_csv(uploadfile2)
            

               
                
                 
                 
                 
             upload_online = [uploadfile1, uploadfile2]
             for file in upload_online:
                 
                 gfile = drive.CreateFile({'x': [{'id': '317538577616-n40l0l6cvnar6bvv8mmks8huk5o80cs4.apps.googleusercontent.com'}]})
                 gfile.SetContentFile(file)
                 gfile.Upload() # Upload the file.
                 os.remove(file)
                       
