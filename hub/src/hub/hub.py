import sys
import calendar
import caching
import ConfigParser
import threading
from traceback import format_exc
import os
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
            self.config.set(name, 'last_update', int(calendar.timegm(dt.utcnow().timetuple())))
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
                set_token(new_token)

        # Update last updated in config file
        timestamp = calendar.timegm(dt.utcnow().timetuple())
        hub.last_updated = timestamp
        hub.config.set('hub', 'last_update', timestamp)
        hub.config_write()

    # Only catching exceptions thrown by requests
    except HTTPError as e:
        # Ignore
        print format_exc()

        # Handle 401 unauthorized, probably because token is outdated.
        # Delete it, effectively forcing a new authentication.
        if e.response.status_code == 401:
            print "Deleting token.."

            set_token("")

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

def set_token(token):
    hub.token = token
    hub.config.set('hub', 'token', token)
    hub.config_write()

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


def config_set(config, section, option):
    value = raw_input('Enter ' + option + ': ')
    config.set(section, option, value)


def create_new_config_file(filename):
    f = open(filename, 'w')
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    config.add_section('hub')
    config.add_section('sensors')
    for option in ['hub_id', 'password', 'server_url', 'server_interval', 'server_wait']:
        config_set(config, 'hub', option)
    config.set('hub', 'last_update', calendar.timegm(dt.utcnow().timetuple()))
    config.set('hub', 'token', '')

    server_url = config.get('hub', 'server_url')
    if server_url[-1] != '/':
        new_url = (server_url + '/')
        config.set('hub', 'server_url', new_url)
    config.write(f)
    f.close()


def check_configuration():
    os.chdir(os.path.dirname(__file__))
    cache_path = "../../cache"
    res_path = "../../res"
    for path in [res_path, cache_path]:
        if not os.path.isdir(path):
            os.makedirs(path)
    os.chdir(res_path)
    config = ConfigParser.RawConfigParser()
    if not os.path.exists(__config_file__):
        print 'No config, making it'
        create_new_config_file(__config_file__)
        # TODO create config file!

    else:
        config.read(__config_file__)
        for section in ['hub', 'sensors']:
            if not config.has_section(section):
                print 'Config file corrupted, please reconfigurate it'
                create_new_config_file(__config_file__)
                break
        config.read(__config_file__)
        options = ['hub_id', 'password', 'last_update', 'server_url', 'server_interval', 'server_wait', 'token']
        missing_options = [option for option in config.items('hub') if option[0] not in options]
        if missing_options:
            print 'missing:', missing_options
            print 'Config file corrupted, please reconfigurate it'
            create_new_config_file(__config_file__)
        config.read(__config_file__)
    config.read(__config_file__)
    return True


def check_for_sensors(a_hub):
    if not a_hub.sensors:
        print 'No sensors found, please add a sensor'
        sensor_name = raw_input('Sensor name: ').lower()
        sensor_type = raw_input('Sensor type: ')
        a_hub.add_sensor(sensor_name, sensor_type)

if __name__ == "__main__":
    sensor_interval = 10  # TODO get this into the config some way
    check_configuration()
    hub = Hub()
    check_for_sensors(hub)
    lock = threading.RLock()
    start_scheduler()
