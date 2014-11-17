import logging
from datetime import datetime as dt


def log_to_console(message):
    """
    Preferred way to print to console and log file. UTC-date is prepended.
    Only for debugging, file will grow forever, must be modified if used in production.
    """
    now = dt.utcnow()
    what_to_log = "[UTC: " + now.strftime("%Y-%m-%d %H:%M:%S") + "] - " + message
    print(what_to_log)

    logging.basicConfig(filename='console_log.log', level=logging.INFO)
    logging.info(what_to_log)
