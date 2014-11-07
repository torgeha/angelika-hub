import logging
from datetime import datetime as dt

"""
Preferred way to print to console. UTC-date is prepended.
Only prints to console for now.

"""

# TODO Add functionality for logging to file (not needed as of now)


def log_to_console(message):
    now = dt.utcnow()
    what_to_log =  "[UTC: " + now.strftime("%Y-%m-%d %H:%M:%S") + "] - " + message
    print what_to_log
    logging.basicConfig(filename='console_log.log', level=logging.INFO)
    logging.info(what_to_log)