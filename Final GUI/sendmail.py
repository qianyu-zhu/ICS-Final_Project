import os,math
import random,sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mailid=sys.argv[1]
digits="0123456789"
OTP=""
for i in range(6):
    OTP+=digits[math.floor(random.random()*10)]
msg='Your OTP Verification for app is '+OTP+' Note..  Please enter otp within 2 minutes and 3 attempts, otherwise it becomes invalid'
file2=open("otp.txt","w")
file2.write(OTP)
file2.close()
# &&&&&&&&&&&&- Your mail id. SENDING OTP FROM mail id
# ************- Your app password. If you do not know how to generate app password for your mail please google.
text = 'Welcome to NYU Chat Room! This is your password for chat access: \n '+OTP+'\n sent using python'
subject='Chat Access Password'
from_email="zqy0927@outlook.com"
to_emails = [mailid]

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

text = 'Welcome to NYU Chat Room! This is your password for chat access: \n'+OTP+'\n sent using python'
send_mail(text, subject='Chat Access Password', from_email="zqy0927@outlook.com", to_emails = ["zqy0927@outlook.com"])

'''
s = smtplib.SMTP('smtp.outlook.com', 587)
s.starttls()
s.login("zqy0927@outlook.com", "Zqy210927")
print(msg)
s.sendmail('zqy0927@outlook.com',mailid,msg)
'''
os.system('python second.py')