import json
import time

__author__ = 'David'
__filename__ = 'cached_data.jsn'
__filepath__ = '../cache/'


def measurements_to_dictionary(measurements):
    measurement_dict = {}
    for m in measurements:
        date = m.date.strftime('%Y-%m-%d')
        measurement = {'type': m.m_type, 'value': m.value, 'unit': m.unit, 'date': int(time.mktime(m.date.timetuple()))}
        measurement_list = measurement_dict.get(date)
        if not measurement_list:
            measurement_list = []
            measurement_dict[date] = measurement_list
        measurement_list.append(measurement)
    return measurement_dict


def write_measurements_to_file(measurements_by_date):
    for date, measurements in measurements_by_date.iteritems():
        filename = __filepath__ + date + ".json"
        f = open(filename, 'w')
        measurement_dictionary = {'Measurements': measurements_by_date[date]}
        json.dump(measurement_dictionary, f, indent=4, sort_keys=True)
        f.close()


def get_old_measurements(measurements):
    d = {}
    for m in measurements:
        date = m.date.strftime('%Y-%m-%d')
        filename = __filepath__ + date + ".json"
        if d.get(date):
            break
        try:
            f = open(filename, 'r')
            json_load = json.load(f)
            f.close()
            d[date] = json_load['Measurements']
        except IOError:
            pass
    return d


def temp(measurements):
    f = open(__filename__, 'w')
    measurement_list = []
    for m in measurements:
        measurement = {'type': m.m_type, 'value': m.value, 'unit': m.unit, 'date': int(time.mktime(m.date.timetuple()))}
        measurement_list.append(measurement)
    json.dump({'Observation': {'hub_id': 1234, 'Measurements': measurement_list}}, f, indent=4, sort_keys=True)


def cache_measurements(measurements):
    temp(measurements)
    old_measurements = get_old_measurements(measurements)
    measurement_dictionary = measurements_to_dictionary(measurements)
    all_measurements = {}
    if old_measurements:
        for date, ms in measurement_dictionary.iteritems():
            old_list = old_measurements.get(date)
            if old_list:
                new = [m for m in ms if m not in old_measurements[date]]
                all_measurements[date] = new + old_list
            else:
                all_measurements[date] = ms
    else:
        all_measurements = measurement_dictionary
    write_measurements_to_file(all_measurements)