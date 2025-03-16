import logging
import logging.config
from datetime import datetime

filetime = datetime.now().strftime('%m%d%y_%H%M%S')

log_config = {
    'version': 1,
    'disable_existing_loggers': False, 
    'formatters': {
        'console_f': {
            'format': '-- %(levelname)s: %(message)s -- %(asctime)s', 
            'datefmt': '%H:%M:%S'
        },
        'file_f': {
            'format': '-- %(levelname)s - %(asctime)s:\n-- -- %(message)s\n',
            'datefmt': '%H:%M:%S--%m-%d-%Y'
        }
    }, 
    'handlers': {
        'stream_h': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_f',
            'level': 'INFO'
        }, 
        'main_file_h': {
            'class': 'logging.FileHandler',
            'filename': f'/programming/Pro-Hoops-ETL/logs/nba_etl.log',
            'formatter': 'file_f',
            'level': 'INFO'
        }, 
        'dtl_file_h': {
            'class': 'logging.FileHandler',
            'filename': f'/programming/Pro-Hoops-ETL/logs/debug/debug_{filetime}.log',
            'formatter': 'file_f',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        '':{
        'handlers': ['stream_h', 'main_file_h', 'dtl_file_h'],
        'level': 'DEBUG',
        'propagate': False
        }
    }
}

def start_logging():
    logging.config.dictConfig(log_config)

# call this function in each module where logging will occur
def get_logger(name=__name__):
    return logging.getLogger(name)

def log_start_msg(logger):
    logger.info(f'LOG STARTED ======================================================')

def log_close_msg(logger):
    logger.info(f'LOG COMPLETE =======================================================')