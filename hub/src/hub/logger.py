from datetime import datetime as dt

"""
Preferred way to print to console. UTC-date is prepended.
Only prints to console for now.

"""

# TODO Add functionality for logging to file (not needed as of now)

def log_to_console(message):
    now = dt.utcnow()
    print "[UTC: " + now.strftime("%Y-%m-%d %H:%M:%S") + "] - " + message