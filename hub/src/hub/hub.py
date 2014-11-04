import sys
import calendar
import caching
import ConfigParser
import threading
from traceback import format_exc
from os import chdir
from datetime import datetime as dt, timedelta
from requests import HTTPError, ConnectionError, Timeout, TooManyRedirects, RequestException
from json_posting import JsonPosting


sys.path.insert(0, '../sensors')
from withings_pulseo2 import WithingsPulseO2


__author__ = 'David'
__version__ = '0.0.1'
__config_file__ = 'hub_config.txt'


class Hub():
    def __init__(self):
        chdir('../../res')  # This is to access the res directory in hub
        self.config = ConfigParser.RawConfigParser()
        self.config.read(__config_file__)
        self.hub_id = self.config.get('hub', 'hub_id')  # Username
        self.last_updated = self.config.getint('hub', 'last_update')
        self.password = self.config.get('hub', 'password')
        self.token = self.config.get('hub', 'token')
        self.server_url = self.config.get('hub', 'server_url')
        self.server_interval = self.config.getint('hub', 'server_interval')
        self.server_wait = self.config.getint('hub', 'server_wait')
        self.sensors = []
        self.json_posting = JsonPosting()
        self.init_sensors()

    def init_sensors(self):
        """
        Initializes and connects to the sensors of this hub
        @return: A list of active sensors that can be interfaced with
        """
        print "Initializing sensors"
        for sensor in self.config.items('sensors'):
            self.sensors.append(self.get_sensor_instance(sensor[0]))
            print "Initialized sensor: " + sensor[0] + "\n"
            # TODO try to connect to BLE sensors

    def get_sensor_instance(self, sensor_name):
        """
        Takes a name to create a new sensor
        The sensor to be created depends on type of sensor, and it must subclass the sensor class
        @param sensor_name: The name of the sensor
        @return: The sensor object for this sensor
        """
        sensor_type = self.config.get(sensor_name, 'type')
        mac_address = self.config.get(sensor_name, 'mac_address')
        if sensor_type == 'withings_pulseo2':
            sensor = WithingsPulseO2(sensor_name)
        sensor.last_updated = self.config.getint(sensor_name, 'last_update')
        return sensor

    def config_write(self):
        config_file = open(__config_file__, 'w')
        self.config.write(config_file)
        config_file.close()

    def add_sensor(self, name, sensor_type, mac_address=None):
        """
        Takes a mac adress and a name and adds it to the list of sensors of this hub
        @param name: The name of the sensor
        @param sensor_type: The type of sensor
        @param mac_address: The MAC address of the sensor
        @return: True if sensor was successfully added to the list, false otherwise
        """
        print "Adding sensor: " + name + ", type: " + sensor_type + ', MAC address: ' + str(mac_address)
        if not [s for s in self.sensors if s.name == name]:
            self.config.set('sensors', name, sensor_type)
            self.config.add_section(name)
            self.config.set(name, 'type', sensor_type)
            self.config.set(name, 'mac_address', mac_address)
            self.config.set(name, 'last_update', int(calendar.timegm((dt.utcnow()-timedelta(days=7)).timetuple())))
            self.config_write()
            self.sensors.append(self.get_sensor_instance(name))
        else:
            print "A sensor with that name already exists"

    def get_sensor_data(self, sensor):
        end_time = dt.utcnow()
        start_time = dt.utcfromtimestamp(sensor.last_updated)
        measurements = sensor.get_all_measurements(start_time, end_time)
        if measurements:
            print 'Caching measurements for', sensor.name
            if caching.cache_measurements(sensor, measurements, self):
                self.config.set(sensor.name, 'last_update', sensor.last_updated)
                self.config_write()
        return measurements

    def get_all_sensor_data(self):
        for sensor in self.sensors:
            measurements = self.get_sensor_data(sensor)
        return measurements


def send_data_to_server():
    filenames = caching.get_old_measurements(hub.last_updated)

    if not filenames:
        print "Nothing to send..."

    token = hub.token
    server_url = hub.server_url
    try:
        for filename in filenames:

            print "sending file: \"" + filename + "\" to server"  # TODO: remove this temporary print

            new_token = hub.json_posting.post_file(filename, hub.hub_id, hub.password, server_url=server_url, token=token)

            if new_token != token:
                hub.token = new_token
                hub.config.set('hub', 'token', new_token)
                hub.config_write()

        # Update last updated in config file
        timestamp = calendar.timegm(dt.utcnow().timetuple())
        hub.last_updated = timestamp
        hub.config.set('hub', 'last_update', timestamp)
        hub.config_write()

    # Only catching exceptions thrown by requests
    except HTTPError:
        # Ignore
        print format_exc()

    except ConnectionError:
        # Ignore
        print format_exc()

    except Timeout:
        # Ignore
        print format_exc()

    except TooManyRedirects:
        # Ignore
        print format_exc()

    except RequestException:  # Fallback if none of the above is caught
        # Ignore
        print format_exc()


def schedule_get_sensor_data(sensor):
    with lock:
        hub.get_sensor_data(sensor)
        threading.Timer(sensor_interval, schedule_get_sensor_data, args=(sensor,)).start()


def schedule_send_server_data():
    
    with lock:
        send_data_to_server()
        threading.Timer(hub.server_interval, schedule_send_server_data).start()


def schedule_delete_old_data():
    caching.delete_old_measurements(calendar.timegm((dt.utcnow()-timedelta(days=7)).timetuple()))
    threading.Timer(60 * 60 * 12, schedule_delete_old_data)  # TODO make this into variable


def start_scheduler():
    for sensor in hub.sensors:
        schedule_get_sensor_data(sensor)
    # wait 20 seconds before sending data to server to allow for sensor to get data
    threading.Timer(hub.server_wait, schedule_send_server_data).start()
    schedule_delete_old_data()


if __name__ == "__main__":
    sensor_interval = 10
    hub = Hub()
    lock = threading.RLock()
    start_scheduler()
