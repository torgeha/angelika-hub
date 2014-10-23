import json
import time

__author__ = 'David'


def cache_measurements(measurements):
    try:
        f = open('cached_data.jsn', 'r+')
    except IOError:
        f = open('cached_data.jsn', 'w')
    for m in measurements:
        d = {'type': m.m_type, 'value': m.value, 'unit': m.unit, 'date': int(time.mktime(m.date.timetuple()))}
        json.dump(d, f)

    f.close()