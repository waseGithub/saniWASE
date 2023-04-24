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
        if '758343539303514031D2' in hwid:
          print('Requested device found 1')
          print(port)
          Megas.append(port)
        else:
          print('specified arduino uno is not connected')
          
print('Megas as port:')          
print(Megas)
         
           

ser1 = serial.Serial(str(ls[0]),  9600, timeout = 100000000)
print("channels correct")
    
time.sleep(25)

if __name__ == '__main__':
   
    
    ser1.flush()
    i = 0
    x = 0

   
    while True:
         i +=1
        # print(i)
    
       
        
         if ser1.in_waiting > 0:
           
             line = ser1.readline().decode("utf-8")
             print(line)
            
             with open ("Sensor_tanklevel.csv","a") as f:
                 x = 1
                 writer = csv.writer(f, delimiter=",")
                 writer.writerow([time.asctime(),line])
                
                
         #######################################
        #######################################
        #change the i value below dependig
        #on how regular updtaes to drive are required  
       #######################################
      #######################################   
                
         if x == 1: 
             print('waiting')
             x = 0
             i = 0
             data = pd.DataFrame()
             upload_file_list = ['Sensor_tanklevel.csv']
             uploadfile = 'Sensor_tanklevel.csv' 
             upload_online = [uploadfile]
             for file in upload_online:
                 
                 gfile = drive.CreateFile({'x': [{'id': '317538577616-n40l0l6cvnar6bvv8mmks8huk5o80cs4.apps.googleusercontent.com'}]})
                 gfile.SetContentFile(file)
                 gfile.Upload() # Upload the file.
                #  os.remove(file)
