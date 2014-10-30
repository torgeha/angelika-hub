import inspect
from traceback import format_exc
from os import chdir
import ConfigParser
import sys
from datetime import datetime as dt, timedelta
import caching
import time
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
        self.hub_id = self.config.get('id', 'hub_id')
        self.sensors = []
        self.init_sensors()

    def init_sensors(self):
        """
        Initializes and connects to the sensors of this hub
        @return: A list of active sensors that can be interfaced with
        """
        print "Initializing sensors"
        for sensor in self.config.items('sensors'):
            self.sensors.append(self.get_sensor(sensor[0]))
            print "Initialized sensor: " + sensor[0] + "\n"
            # TODO try to connect to ble sensors

    def get_sensor(self, sensor_name):
        """
        Takes a name to create a new sensor
        The sensor to be created depends on type of sensor, and it must subclass the sensor class
        @param sensor_name: The name of the sensor
        @return: The sensor object for this sensor
        """
        sensor_type = self.config.get(sensor_name, 'type')
        # MAC not used by withings sensor, but should be used for BLE devices
        mac_address = self.config.get(sensor_name, 'mac_address')
        if sensor_type == 'withings_pulseo2':
            sensor = WithingsPulseO2(sensor_name)
            sensor.last_updated = self.config.getint(sensor_name, 'last_update')
            return sensor

    def search_for_sensors(self):
        """
        Searches for sensors and returns a list of BLE sensors
        """
        print "(not really) Searching for sensors ...\nNo sensors found\n"
        # TODO: use gatttool lescan to search for BLE devices and return a list (or similar) of them.

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
            self.config.set(name, 'last_update', int(time.mktime((dt.utcnow()-timedelta(days=7)).timetuple())))
            self.config_write()
            self.sensors.append(self.get_sensor(name))
        else:
            print "A sensor with that name already exists"

    def get_sensors(self):
        """
        This function returns a list of the currently connected sensors
        @return:
        """
        print "sensors:" + str(self.sensors)
        return self.sensors

    def get_all_sensor_data(self):
        end_time = dt.utcnow()
        for sensor in self.sensors:
            start_time = dt.utcfromtimestamp(sensor.last_updated)
            measurements = sensor.get_all_measurements(start_time, end_time)
            if measurements:
                if caching.cache_measurements(sensor, measurements, self):
                    self.config.set(sensor.name, 'last_update', sensor.last_updated)
                    self.config_write()
        return measurements


def print_help():
    """
    Prints what functions are allowed to use
    """
    print "Usage: action [arguments]: function"
    for k, v in program_functions.iteritems():
        args = inspect.getargspec(v).args
        if args and args[0] == 'self':
            del args[0]
        print k + " " + str(args) + ": " + v.__name__


program_functions = {'s': Hub.search_for_sensors,
                     'l': Hub.get_sensors,
                     'a': Hub.add_sensor,
                     'h': print_help,
                     'g': Hub.get_all_sensor_data}
hub = Hub()


def main():
    """
    The main method of the hub. This is where the magic happens
    """
    while True:
        raw_program_input = raw_input("angelika_hub_" + __version__ + "> ")
        if raw_program_input == "" or raw_program_input == "exit":
            break
        program_input = str.split(raw_program_input, " ", 1)
        program_function = program_functions.get(program_input[0])
        arguments = []
        if hasattr(program_function, 'im_class'):
            if program_function.im_class == Hub:
                arguments.append(hub)
        try:
            if len(program_input) > 1:
                arguments += (str.split(program_input[1]))
            if len(arguments) > 0:
                program_function(*arguments)
            else:
                program_function()
        except TypeError:
            print "Error, probably wrong number of arguments"
            print format_exc()
    print "Terminating..."
    # TODO: terminate hub


if __name__ == "__main__":
    main()
