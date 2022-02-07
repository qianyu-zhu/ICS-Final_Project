import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from tkinter import *
from tkinter import messagebox

# environment variables
username = "zqy0927@outlook.com"
password = "Zqy210927"

def send_mail(text='Email Body', subject='Hello World', from_email='Chat Room <zqy0927@outlook.com>', to_emails=None):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    msg_str = msg.as_string()
    # login to my smtp server
    server = smtplib.SMTP(host='smtp.outlook.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()
    # with smtplib.SMTP() as server:
    #     server.login()
    #     pass

text = 'Welcome to NYU Chat Room! This is your password for chat access: \n 2ft@$hiA \n sent using python'
send_mail(text, subject='Chat Access Password', from_email="zqy0927@outlook.com", to_emails = ["zqy0927@outlook.com"])