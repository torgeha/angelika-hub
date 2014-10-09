from withings import *
import ConfigParser
import os
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
values = {}
values["pulse"] = []
values["ox"] = []
for m in measures:
    pulse = m.get_measure(11)
    ox_sat = m.get_measure(54)
    if pulse is not None:
        values["pulse"].append((pulse, str(m.date)))
    if ox_sat is not None:
        values["ox"].append((ox_sat, str(m.date)))
print values
