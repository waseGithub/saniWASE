import serial
import time
import csv
import serial.tools.list_ports
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  

time.sleep(2)
if __name__ == '__main__':
    
    ports = serial.tools.list_ports.comports(include_links =False)
    ls = []
    for port in ports:
        print(port.device)
        ls.append(port.device)
    

    ser1 = serial.Serial(str(ls[0]),  38400, timeout = 25)
    ser2 = serial.Serial(str(ls[1]),  38400, timeout = 25)
    ser3 = serial.Serial(str(ls[2]),  38400, timeout = 25)
    ser4 = serial.Serial(str(ls[3]),  38400, timeout = 25)
    print("channels correct")
   
    
   
    
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
            
         if i == 50000 :
             i = 0
             upload_file_list = ['Sensor_A.csv', 'Sensor_B.csv', 'Sensor_C.csv','Sensor_D.csv']
             for upload_file in upload_file_list:
                 
                 gfile = drive.CreateFile({'x': [{'id': '317538577616-n40l0l6cvnar6bvv8mmks8huk5o80cs4.apps.googleusercontent.com'}]})
                 gfile.SetContentFile(upload_file)
                 gfile.Upload() # Upload the file.
                 
                       
                     

             
                  
                        
           
         
