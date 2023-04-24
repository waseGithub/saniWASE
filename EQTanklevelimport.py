import serial

arduino_port = "/dev/ttyACM4"
baud = 9600
fileName="EQ-tank-level.csv"

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port: " + arduino_port)
file = open(fileName, "a")
print("Created file")

#display the data to the terminal
getData=str(ser.readline())
data=getData[0:][:-2]
print(data)

#add the data to the file
file = open(fileName, "a") #append the data to the file
file.write(data + "\\n") #write data with a newline

#close out the file
file.close()
