import json
import time
from traceback import format_exc

__author__ = 'David'
__filename__ = 'cached_data.jsn'


def measurements_to_list(measurements):
    measurement_list = []
    for m in measurements:
        measurement = {'type': m.m_type, 'value': m.value, 'unit': m.unit, 'date': int(time.mktime(m.date.timetuple()))}
        measurement_list.append(measurement)
    return measurement_list


def write_measurements_to_file(measurement_list):
    f = open(__filename__, 'w')
    measurement_dictionary = {'Measurements': measurement_list}
    json.dump(measurement_dictionary, f, indent=4, sort_keys=True)
    f.close()


def get_old_measurements():
    f = open(__filename__, 'r')
    json_load = json.load(f)
    f.close()
    return json_load['Measurements']


def cache_measurements(measurements):
    try:
        old_measurements = get_old_measurements()
    except IOError:
        old_measurements = []
        print "Couldn't read file"
        print format_exc()
    measurement_list = measurements_to_list(measurements)
    new_measurements = []
    if old_measurements:
        for m in measurement_list:
            if m not in old_measurements:
                new_measurements.append(m)
    else:
        new_measurements = measurement_list
    write_measurements_to_file(old_measurements + new_measurements)