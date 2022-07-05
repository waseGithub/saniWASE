import subprocess
  
  
pytonProcess = subprocess.check_output("ps -ef | grep .py",shell=True).decode()
pytonProcess = pytonProcess.split('\n')

found = False 
for process in pytonProcess:
    print(process)
    if "combined.py" in process: 
      print('process found')
      found = True
      break
if found == False:
  print('data script not running')
