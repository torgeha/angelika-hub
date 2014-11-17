from withings import *
import ConfigParser
import calendar
from sensors import Sensor, Measurement


class WithingsPulseO2(Sensor):
    MEASURE_TYPES = {11: 'heart_rate', 54: 'spo2'}
    VALUE_UNITS = {11: 'bpm', 54: 'percent', 'steps': 'steps', 'distance': 'm', 'elevation': 'm',
                   'soft': 's', 'moderate': 's', 'intense': 's', 'calories': 'kcal'}

    def __init__(self, name):
        self._name = name
        self._last_updated = 946684800  # 2000.01.01
        config = ConfigParser.RawConfigParser()
        # Tries to access the res directory in hub
        try:
            config.read('oauth_pulseO2.txt')
            config.get('keys', 'oauth_token')
        except ConfigParser.NoSectionError:
            config.read('../../res/oauth_pulseO2.txt')

        access_token = config.get('keys', 'oauth_token')
        access_token_secret = config.get('keys', 'oauth_token_secret')
        consumer_key = config.get('keys', 'consumer_key')
        consumer_secret = config.get('keys', 'consumer_secret')
        user_id = config.get('keys', 'userid')

        creds = WithingsCredentials(access_token, access_token_secret, consumer_key,
                                    consumer_secret, user_id)
        self.client = WithingsApi(creds)

    @property
    def name(self):
        return self._name

    @property
    def last_updated(self):
        return self._last_updated

    @last_updated.setter
    def last_updated(self, value):
        self._last_updated = value

    @name.setter
    def name(self, value):
        self._name = value

    def get_all_measurements(self, start_date, end_date):
        measure_group = self.client.get_measures(startdate=calendar.timegm(start_date.timetuple()),
                                                 enddate=calendar.timegm(end_date.timetuple()))
        activity_group = self.client.get_activities(startdateymd=start_date.strftime('%Y-%m-%d'),
                                                    enddateymd=end_date.strftime('%Y-%m-%d'))
        measurements = []
        for activities in activity_group:
            for name, value in activities.activities.iteritems():
                measurements.append(
                    Measurement(name, value, self.VALUE_UNITS[name], activities.date))
        for measures in measure_group:
            for m in measures.measures:
                if self.MEASURE_TYPES.get(m['type']):
                    measurements.append(Measurement(self.MEASURE_TYPES[m['type']], m['value'],
                                                    self.VALUE_UNITS[m['type']], measures.date))
        return sorted(measurements, key=lambda measurement: measurement.date)
