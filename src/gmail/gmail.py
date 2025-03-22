import os
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
from pathlib import Path
from datetime import datetime
from gmail.gmail_config import sender, receiver, password, server, port

gmail_log_path = '/home/jdeto/programming/nba_etl/nba_current/src/gmail/logs/'

def get_recent_log(dir):
    ls = glob.glob(os.path.join(dir, '*'))
    if not ls:
        return None
    return max(ls, key=os.path.getmtime)

def start_gmail_log():
    ftime = datetime.now().strftime('%m%d%Y_%H-%M')
    file = Path(f'{gmail_log_path}nba_etl_{ftime}.txt')
    if not file.exists():
        with open(file, 'a') as f:
            f.write(f'NBA ETL started - {datetime.today().strftime("%m/%d/%Y %H:%M")}\n')        
    return file

def gmail_log_write(file, msg):
        with open(file, 'a') as f:
            f.write(msg)
    
def send_summary():
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = f'NBA ETL complete - {datetime.today().strftime("%m/%d/%Y %H:%M")}'
    body = MIMEText(f'Insert summaries attached')
    msg.attach(body)
    
    with open(get_recent_log(gmail_log_path), 'rb') as f:
        msg.attach(MIMEApplication(f.read(), name='nba_etl_summary.txt'))
        
    with smtplib.SMTP_SSL(server, port) as gmail:
        gmail.login(sender, password)
        gmail.sendmail(sender, receiver, msg.as_string())
    