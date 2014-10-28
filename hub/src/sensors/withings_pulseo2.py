from withings import *
import ConfigParser
import os
import time
from sensor import Sensor, Measurement


class WithingsPulseO2(Sensor):
    MEASURE_TYPES = {11: 'heart_rate', 54: 'spo2'}
    VALUE_UNITS = {11: 'bpm', 54: 'percent', 'steps': 'steps', 'distance': 'm', 'elevation': 'm', 'soft': 's',
                   'moderate': 's', 'intense': 's', 'calories': 'kcal'}

    def __init__(self, name):
        self.name = name
        config = ConfigParser.RawConfigParser()
        # Tries to access the res directory in hub
        try:
            config.read('oauth_pulse02.txt')
            config.get('keys', 'oauth_token')
        except ConfigParser.NoSectionError:
            config.read('../../res/oauth_pulse02.txt')

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
                measurements.append(Measurement(name, value, self.VALUE_UNITS[name], activities.date))
        for measures in measure_group:
            for m in measures.measures:
                if self.MEASURE_TYPES.get(m['type']):
                    measurements.append(Measurement(self.MEASURE_TYPES[m['type']], m['value'],
                                                    self.VALUE_UNITS[m['type']], measures.date))
        return sorted(measurements, key=lambda measurement: measurement.date)







