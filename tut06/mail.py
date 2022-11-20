import smtplib
from mimetypes import guess_type
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

start_time = datetime.now()

def send_mail(fromaddr, frompasswd, toaddr, msg_subject, msg_body, filename, filepath):
    try:
        msg = MIMEMultipart()
        print("[+] Message Object Created")
    except:
        print("[-] Error in Creating Message Object")
        return

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = msg_subject

    body = msg_body

    msg.attach(MIMEText(body, 'plain'))
    
    attachment = open(filepath, "rb")

    mimetype,encoding = guess_type(filename)
    mimetype = mimetype.split('/', 1)
    
    p = MIMEBase(mimetype[0], mimetype[1])
    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    try:
        msg.attach(p)
        print("[+] File Attached")
    except:
        print("[-] Error in Attaching file")
        return

    try:
        # s = smtplib.SMTP('smtp.gmail.com', 587)
        s = smtplib.SMTP('stud.iitp.ac.in', 587)
        print("[+] SMTP Session Created")
    except:
        print("[-] Error in creating SMTP session")
        return

    s.starttls()

    try:
        s.login(fromaddr, frompasswd)
        print("[+] Login Successful")
    except:
        print("[-] Login Failed")

    text = msg.as_string()

    try:
        s.sendmail(fromaddr, toaddr, text)
        print("[+] Mail Sent successfully")
    except:
        print('[-] Mail not sent')

    s.quit()

def isEmail(x):
    if ('@' in x) and ('.' in x):
        return True
    else:
        return False

def sendreport():
    FROM_ADDR = "aarav_2001me01@iitp.ac.in"
    FROM_PASSWD = "changeme"
    TO_ADDR = "cs3842022@gmail.com"

    Subject = "Consolidated Report"

    Body ='''
    Consolidated Attendance Report sent as attachment
    '''

    filepath = './output/attendance_report_consolidated.xlsx'
    filename = 'attendance_report_consolidated.xlsx'
    if(isEmail(FROM_ADDR) and isEmail(TO_ADDR)):
        send_mail(FROM_ADDR, FROM_PASSWD, TO_ADDR, Subject, Body, filename, filepath)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))