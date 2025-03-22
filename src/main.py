from data.fetch import fetch_insert_glogs_pbp
from log_config.logs import start_logging, get_logger, log_start_msg, log_close_msg
from gmail.gmail import start_gmail_log, send_summary

# PASS DAYS=1, DAYS_BACK=1 FOR THE NIGHTLY SCRIPT

def main():
    start_logging()
    gmail_log = start_gmail_log()
    
    logger = get_logger(__name__)
    log_start_msg(logger)
    
    # this calls all functions in other modules - running this fetches, cleans, and inserts all data
    fetch_insert_glogs_pbp(gmail_log, days=1, days_back=1)
    
    log_close_msg(logger)
    
    # sends txt summary via gmail
    send_summary()
    
if __name__=='__main__':
    main()
