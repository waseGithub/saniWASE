import subprocess
import yagmail
import time
import smtplib
gmail_user = 'autonomousemail1@gmail.com'
gmail_password = 'odqcdosrnoipmxmd'
  
  
pytonProcess = subprocess.check_output("ps -ef | grep .py",shell=True).decode()
pytonProcess = pytonProcess.split('\n')
sent_from = gmail_user
to = ['hcrutland@mail.com']
subject = 'test email'
body = 'this is a test'


global first
global found
first = True
found = False

while(1):
  time.sleep(3)

  for process in pytonProcess:
    
#       print(process)
      if "combined.py" in process: 
        print('combined.py process found')
        found = True
        first = True
      else:
        print('combined.py process not found')
        found = False
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

 


