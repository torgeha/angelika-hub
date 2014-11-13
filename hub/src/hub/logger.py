import logging
import logging.handlers
from datetime import datetime as dt

"""
Preferred way to print to console and log file. UTC-date is prepended.
"""

def log_to_console(message):
    now = dt.utcnow()
    what_to_log =  "[UTC: " + now.strftime("%Y-%m-%d %H:%M:%S") + "] - " + message
    print what_to_log
    
    log_filename = 'console_log.log'
    
    hub_logger = logging.getLogger('hub_logger')
    hub_logger.setLevel(logging.INFO)
    
    # A log file does not exceed 1MB and 5 files are kept before deleting them.
    handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1000000, backupCount=5)
    hub_logger.addHandler(handler)
    
    hub_logger.info(what_to_log)
    
