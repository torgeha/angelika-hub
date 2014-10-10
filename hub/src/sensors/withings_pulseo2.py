from withings import *
import ConfigParser
import os
import time
from sensor import Sensor, Measurement


class WithingsPulseO2(Sensor):
    def __init__(self):
        os.chdir('../../res')  # This is to access the res directory in hub
        config = ConfigParser.RawConfigParser()
        config.read('oauth_pulse02.txt')

        access_token = config.get('keys', 'oauth_token')
        access_token_secret = config.get('keys', 'oauth_token_secret')
        consumer_key = config.get('keys', 'consumer_key')
        consumer_secret = config.get('keys', 'consumer_secret')
        user_id = config.get('keys', 'userid')

        creds = WithingsCredentials(access_token, access_token_secret, consumer_key, consumer_secret, user_id)
        self.client = WithingsApi(creds)

    def get_all_measurements(self, start_date, end_date):
        measure_group = self.client.get_measures(startdate=time.mktime(start_date.timetuple()),
                                                 enddate=time.mktime(end_date.timetuple()))
        activity_group = self.client.get_activities(startdateymd=start_date.strftime('%Y-%m-%d'),
                                                    enddateymd=end_date.strftime('%Y-%m-%d'))
        measurements = []
        for activities in activity_group:
            for name, value in activities.activities.iteritems():
                measurements.append(Measurement(name, value, "NA", activities.date))
        for measures in measure_group:
            for m in measures.measures:
                measurements.append(Measurement(m['type'], m['value'], "NA", measures.date))
        return measurements







