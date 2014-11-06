# -*- coding: utf-8 -*-
# Send email to specified email addresses containing ip taken as argument
import sys
import smtplib
from email.mime.text import MIMEText
import datetime

#Append additional recipients to this list
to = ['email@placeholder.com', 'email2@placeholder.com']
gmail_user = 'angelikarasp@gmail.com'
gmail_password = 'Enter password here'  # password for the email
smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)
today = datetime.date.today()

ipaddr = sys.argv[1]
global_ip_addr = "Not found"

if len(sys.argv) > 2:
  global_ip_addr = sys.argv[2]

mail_content = "My IP is: "
my_ip = mail_content + ipaddr + "\n" + "Global IP: " + global_ip_addr
msg = MIMEText(my_ip)
subject_cont = "AngelikaRasp's IP on "
subject_date = today.strftime('%b %d %Y')
msg['Subject'] = subject_cont + subject_date
msg['From'] = gmail_user

msg['To'] = ', '.join(to)

smtpserver.sendmail(gmail_user, to, msg.as_string())
smtpserver.quit()
