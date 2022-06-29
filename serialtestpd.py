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




     
       


ports = serial.tools.list_ports.comports(include_links =False)
ls = []
for port in ports:
    print(port.device)
    ls.append(port.device)
   
print(ls)


import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

Megas = []
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        if '7583435393035160F0C1' in hwid:
          print('Requested device found 1')
          print(port)
          Megas.append(port)
        elif '5583931353835151B072' in hwid:
          print('Requested device found 2')
          print(port)
          Megas.append(port)
        elif '8503731383535161A180' in hwid:
          print('Requested device found 3')
          print(port)
          Megas.append(port)
        elif '5503731333735150D090' in hwid:
          print('Requested device found 4')
          print(port)
          Megas.append(port)
          
print('Megas as port:')          
print(Megas)
         
           

ser1 = serial.Serial(str(ls[0]),  38400, timeout = 25)
ser2 = serial.Serial(str(ls[4]),  38400, timeout = 25)
ser3 = serial.Serial(str(ls[2]),  38400, timeout = 25)
ser4 = serial.Serial(str(ls[3]),  38400, timeout = 25)
print("channels correct")
    
time.sleep(25)

if __name__ == '__main__':
    
   
   
    
   
    
    ser1.flush()
    ser2.flush()
    ser3.flush()
    ser4.flush()
    i = 0

   
    while True:
         i +=1
         print(i)
    
       
        
         if ser1.in_waiting > 0:
           
             line = ser1.readline().decode("utf-8")
             print(line)
            
             with open ("Sensor_A.csv","a") as f:
                
                 writer = csv.writer(f, delimiter=",")
                 writer.writerow([time.asctime(),line])
                

         if ser2.in_waiting > 0:
           
             line = ser2.readline().decode("utf-8")
             print(line)
            
             with open ("Sensor_B.csv","a") as f:
                
                 writer = csv.writer(f, delimiter=",")
                 writer.writerow([time.asctime(),line])
                
                
                
         if ser3.in_waiting > 0:
           
            line = ser3.readline().decode("utf-8")
            print(line)
            
            with open ("Sensor_C.csv","a") as f:
                
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.asctime(),line])
         
                
         if ser4.in_waiting > 0:
           
            line = ser4.readline().decode("utf-8")
            print(line)
            
            with open ("Sensor_D.csv","a") as f:
                
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.asctime(),line])
                
         #######################################
        #######################################
        #change the i value below dependig
        #on how regular updtaes to drive are required  
       #######################################
      #######################################   
                
         if i == 7500: 
             i = 0
             data = pd.DataFrame()
             upload_file_list = ['Sensor_A.csv', 'Sensor_B.csv', 'Sensor_C.csv','Sensor_D.csv']
             colnames = ['datetime','vals']
             for upload_file in upload_file_list:
                 df = pd.read_csv(upload_file,index_col=0, skiprows=5, names = colnames)
                 data = data.append(df)
                 os.remove(upload_file)
             data.index = pd.to_datetime(data.index, format="%a %b %d %X %Y")
             data[['ID','CH4','CO2','OH','Cnt']]= data.loc[:,'vals'].str.split(',',4, expand =True)
             data.reset_index(inplace =True)
             data.drop('vals',axis=1, inplace=True)
             data.set_index(['ID', 'datetime'], inplace = True)
             data = data[::200]
             curr = time.time()
             curr = time.ctime(curr) 
             uploadfile = 'sensor_all_' + str(curr) + '.csv'
             data.to_csv(uploadfile)
             
           
                 
                 
                 
             upload_online = [uploadfile]
             for file in upload_online:
                 
                 gfile = drive.CreateFile({'x': [{'id': '317538577616-n40l0l6cvnar6bvv8mmks8huk5o80cs4.apps.googleusercontent.com'}]})
                 gfile.SetContentFile(file)
                 gfile.Upload() # Upload the file.
                 os.remove(file)
                       
                     

             
                  
                        
           
         
