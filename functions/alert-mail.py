""" import smtplib


subject = "NEW ELEMENT DICOVERED"
text = "yo"

message = 'Subject: {}\n\n{}'.format(subject, text)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(sender, password)
    print("Login Succesfull")
    server.sendmail(sender, receiver, message)
    print("Email was Sent")
    server.close()
except:
    print("Error Logging in")
 """

import smtplib, ssl
from email.mime.text import MIMEText

def send_email(temperature):
    port = 465  # For SSL
    password = ""
    sender_email = ""
    receiver_email = ""
    message = MIMEText(" needs 1M aether and these 4 elements")
    message['Subject'] = "%0.2f was DISCOVERED!!3" % temperature
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", port)
        server.login(sender_email, password)
        print("Login Succesfull")
        server.sendmail(sender_email, [receiver_email], message.as_string())
        print("Email was Sent")
        server.quit()
    except:
        print("Error Logging in")


send_email(6)