import json
import time
from datetime import datetime as dt

__author__ = 'David'
__filename__ = 'cached_data.jsn'
__filepath__ = '../cache/'


def measurements_to_dictionaries(measurements):
    measurement_list = []
    for m in measurements:
        measurement = {'type': m.m_type, 'value': m.value, 'unit': m.unit, 'date': int(time.mktime(m.date.timetuple()))}
        measurement_list.append(measurement)
    return measurement_list


def write_measurements_to_file(sensor, measurements):
    utc_now = int(time.mktime(dt.utcnow().timetuple()))
    sensor.last_updated = utc_now
    filename = __filepath__ + sensor.name + str(utc_now) + ".json"
    f = open(filename, 'w')
    measurement_dictionary = {'Measurements': measurements}
    json.dump(measurement_dictionary, f, indent=4, sort_keys=True)
    f.close()


def get_old_measurements(last_update):
    pass
    #TODO make this method look for measurements not yet sent to server


def temp(measurements):
    f = open(__filename__, 'w')
    measurement_list = []
    for m in measurements:
        measurement = {'type': m.m_type, 'value': m.value, 'unit': m.unit, 'date': int(time.mktime(m.date.timetuple()))}
        measurement_list.append(measurement)
    json.dump({'Observation': {'hub_id': 1234, 'Measurements': measurement_list}}, f, indent=4, sort_keys=True)


def cache_measurements(sensor, measurements):
    temp(measurements)
    measurement_dictionaries = measurements_to_dictionaries(measurements)
    write_measurements_to_file(sensor, measurement_dictionaries)
    return True