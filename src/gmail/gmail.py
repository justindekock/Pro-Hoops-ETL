import os
import glob
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl
import smtplib
from pathlib import Path
from datetime import datetime, timedelta
from gmail.gmail_config import sender, receiver, password, server, port
#from database.dba import select_count

# TODO - get it to attach the log

RUNTIME = datetime.now().strftime('%m/%d/%Y %H:%M')

gmail_log_path = '/home/jdeto/programming/nba_etl/nba_current/src/gmail/logs/'



def get_recent_log(dir):
    ls = glob.glob(os.path.join(dir, '*'))
    if not ls:
        return None
    return max(ls, key=os.path.getmtime)
    # nfile = max(ls, key=os.path.getmtime)
    # return nfile

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
        

def send_email(subject, body):

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())
        
# send_email('test function', 'this is a test body')

class GmailBody:
    def __init__(self):
        self.body = self.construct(self.get_dates(),
                                   self.get_counts())


    def construct(dates, counts):
        f"""
NBA ETL complete -- {dates[0]}
-- Games played on {dates[1]}
-- {counts[0]} new games inserted 
-- -- {counts[1]} unique games after insert
-- {counts[2]} new game logs inserted 
-- -- {counts[3]} unique game logs after insert
-- {counts[4]} new play-by-play records inserted 
-- -- {counts[5]} unique rows after insert

"""

    def get_dates(self):
        return [datetime.now().strftime('%m/%d/%Y %H:%M'), (datetime.today() - timedelta(1)).strftime('%m/%d/%Y %H:%M')]
    
    def pre_counts(self):
        return [select_count('game'),
                select_count('player_box'), 
                select_count('playbyplay')]

    def get_counts():
        pass 
    
class Body:
    def __init__(self, game_date, new_games, new_logs, new_pbp, 
                 tot_games, tot_logs, tot_pbp):
        self.body = f"""

-- Games played on {game_date}
-- {new_games} new games inserted 
-- -- {tot_games} unique games after insert
-- {new_logs} new game logs inserted 
-- -- {tot_logs} unique game logs after insert
-- {new_pbp} new play-by-play records inserted 
-- -- {tot_pbp} unique rows after insert
"""
        
        
        
# body = Body('03/21/2025', 10, 214, 4298, 1045, 24587, 452308)
# print(body.body)


