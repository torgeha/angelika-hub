import logging
import logging.handlers
from datetime import datetime as dt

"""
Preferred way to print to console and log file. UTC-date is prepended.
"""
        
import logging
import logging.handlers
from datetime import datetime as dt
   
log_filename = 'console_log.log'
h_logger = logging.getLogger('hub_logger')
h_logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1000000, backupCount=5)
h_logger.addHandler(handler)

def log_to_console(message):
    now = dt.utcnow()
    what_to_log =  "[UTC: " + now.strftime("%Y-%m-%d %H:%M:%S") + "] - " + message
    print(what_to_log)
        
    h_logger.info(what_to_log)

        
