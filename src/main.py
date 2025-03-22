from data.fetch import fetch_insert_glogs_pbp
from log_config.logs import start_logging, get_logger, log_start_msg, log_close_msg
from gmail.gmail import start_gmail_log, send_summary

# PASS DAYS=1, DAYS_BACK=1 FOR THE NIGHTLY SCRIPT
# TO RUN THE FUNCTION FOR SEVERAL DAYS, PASS NUMBER OF DAYS DESIRED TO DAYS
# TO START ON A DAY OTHER THAN YESTERDAY, PASS >0 TO DAYS_BACK
# DAYS=10, DAYS_BACK=5 WOULD START AT 5 DAYS AGO AND FETCH FOR 10 DAYS GOING BACK 

def main():
    # initiate the logger
    start_logging()
    gmail_log = start_gmail_log()
    
    logger = get_logger(__name__)
    log_start_msg(logger)
    
    # this calls all functions in other modules - running this fetches, cleans, and inserts all data
    fetch_insert_glogs_pbp(gmail_log, days=1, days_back=1)
    
    
    
    log_close_msg(logger)
    # gmail_log_path = '/home/jdeto/programming/nba_etl/nba_current/src/gmail/logs/'
    # print(get_recent_log(gmail_log_path))
    
    send_summary()
    
if __name__=='__main__':
    main()
