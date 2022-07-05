import subprocess
import yagmail
# import smtplib
# from email.mime.text import MIMEText
  
  
pytonProcess = subprocess.check_output("ps -ef | grep .py",shell=True).decode()
pytonProcess = pytonProcess.split('\n')




found = False 
for process in pytonProcess:
    print(process)
    if "combine.py" in process: 
      print('process found')
      found = True
      break
if found == False:
  print('data script not running')
#   with open('error_msg_combined.txt', 'rb') as fp:
#       # Create a text/plain message
#       msg = MIMEText(fp.read())
#       msg['Subject'] = 'script:combined.py failure on systems:linux at site:saniwase_hepworth'
#       msg['From'] = harvey.rutland@wase.co.uk
#       msg['To'] = william.gambier@wase.co.uk

#       # Send the message via our own SMTP server, but don't include the
#       # envelope header.
#       s = smtplib.SMTP('localhost')
#       s.sendmail(me, [you], msg.as_string())
#       s.quit()
  
  yag = yagmail.SMTP('intern.wase', '69methane69')
  yag.send('hcrutland@mail.com', 'test', 'test')
