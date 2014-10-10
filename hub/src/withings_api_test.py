from withings import *
import ConfigParser
import os
from datetime import date, timedelta
os.chdir('../res')  # This is to access the res directory in hub

config = ConfigParser.RawConfigParser()
config.read('oauth_pulse02.txt')

access_token = config.get('keys', 'oauth_token')
access_token_secret = config.get('keys', 'oauth_token_secret')
consumer_key = config.get('keys', 'consumer_key')
consumer_secret = config.get('keys', 'consumer_secret')
user_id = config.get('keys', 'userid')

creds = WithingsCredentials(access_token, access_token_secret, consumer_key, consumer_secret, user_id)
client = WithingsApi(creds)
measures = client.get_measures()
today = date.today()
lastUpdate = date.today() - timedelta(days=0)
activities = client.get_activities(startdateymd=lastUpdate.strftime('%Y-%m-%d'),
                                   enddateymd=date.today().strftime('%Y-%m-%d'))