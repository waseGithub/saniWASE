import subprocess
import yagmail
import time
import smtplib
gmail_user = 'autonomousemail1@gmail.com'
gmail_password = 'odqcdosrnoipmxmd'
  
  

sent_from = gmail_user
to = ['william.gambier@wase.co.uk']
subject = 'error report- script:combined.py site:saniwase_linux'
body = 'Data script combined.py it not recording data-- Script description: logging gas flow / percentage, and tank level data to google drive intern account'


global first
global found
first = True
found = False

while(1):
  pytonProcess = subprocess.check_output("ps -ef | grep .py",shell=True).decode()
  pytonProcess = pytonProcess.split('\n')
  time.sleep(3)
  
  found = False
  
  for process in pytonProcess:
    
#       print(process)
      if "combined.py" in process: 
        print('combined.py process found')
        found = True
        first = True
        continue
      else:
        print('-')

  
#   print(found)
  if found == False:
    print('data script not running')
    if first == True:
      first = False 
      email_text = """\
      From: %s
      To: %s
      Subject: %s
      %s
      """ % (sent_from, ", ".join(to), subject, body)
      try:
          smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
          smtp_server.ehlo()
          smtp_server.login(gmail_user, gmail_password)
          smtp_server.sendmail(sent_from, to, email_text)
          smtp_server.close()
          print ("Email sent successfully!")
          time.sleep(10)
      except Exception as ex:
          print ("Something went wrong….",ex)

 


