import smtplib, ssl

port = 465  # For SSL
password = '69methane69'

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("intern.wasetech@gmail.com", password)
    # TODO: Send email here
