import json
import calendar
from datetime import datetime as dt
import os

__author__ = 'David'
__filepath__ = '../cache/'


def measurements_to_dictionaries(measurements):
    measurement_list = []
    for m in measurements:
        measurement = {'type': m.m_type, 'value': m.value, 'unit': m.unit, 'date': int(calendar.timegm(m.date.timetuple()))}
        measurement_list.append(measurement)
    return measurement_list


def get_new_measurements(sensor, measurements):
    all_filenames = next(os.walk(__filepath__))[2]
    sensor_filenames = [name for name in all_filenames if sensor.name in name]
    old_measurements = []
    for filename in sensor_filenames:
        f = open(__filepath__ + filename, 'r')
        old_measurements += json.load(f)['Measurements']
        f.close()
    new_measurements = [m for m in measurements if m not in old_measurements]
    return new_measurements


def write_measurements_to_file(sensor, measurements, hub):
    max_date = sensor.last_updated
    for m in measurements:
        max_date = max(max_date, m['date'])
    sensor.last_updated = max_date
    new_measurements = get_new_measurements(sensor, measurements)
    if not new_measurements:
        print "No new measurements"
        return False
    utc_now = int(calendar.timegm(dt.utcnow().timetuple()))
    filename = __filepath__ + str(utc_now) + "_" + sensor.name + ".json"
    f = open(filename, 'w')
    measurement_dictionary = {'Observation': {'hub_id': hub.hub_id}, 'Measurements': new_measurements}
    json.dump(measurement_dictionary, f, indent=4, sort_keys=True)
    f.close()
    return True


def get_old_measurements(last_update):
    files_not_sent = []
    filenames = next(os.walk(__filepath__))[2]
    for filename in filenames:
        date = int(filename[0:filename.index('_')])
        if date > last_update:
            files_not_sent.append(os.path.dirname(os.path.abspath(__filepath__ + filename)) + '/' + filename)
    return files_not_sent


def delete_old_measurements(timestamp):
    filenames = next(os.walk(__filepath__))[2]
    for filename in filenames:
        date = int(filename[0:filename.index('_')])
        if date < timestamp:
            os.remove(__filepath__ + '/' + filename)


def cache_measurements(sensor, measurements, hub):
    measurement_dictionaries = measurements_to_dictionaries(measurements)
    return write_measurements_to_file(sensor, measurement_dictionaries, hub)