from data.fetch import run_many_days
from log_config.logs import start_logging, get_logger, log_start_msg, log_close_msg

def main():
    # initiate the logger
    start_logging()
    logger = get_logger(__name__)
    log_start_msg(logger)
    # pass number of days to pass (default 1)
    run_many_days(1) # defined in fetch - calls several functions from there

    log_close_msg(logger)
    
if __name__=='__main__':
    main()