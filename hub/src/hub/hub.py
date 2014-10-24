import inspect
from traceback import format_exc
from os import chdir
import ConfigParser
import sys
from datetime import datetime as dt, timedelta
import caching
sys.path.insert(0, '../sensors')
from withings_pulseo2 import WithingsPulseO2


__author__ = 'David'
__version__ = "0.0.1"


def get_sensor(sensor_name, mac_address=0):
    """
    Takes a name and an optianal MAC adress to create a new sensor
    The sensor to be created depends on the name, and it must subclass the sensor class
    @param sensor_name: The name of the sensor
    @param mac_address: The mac address of the sensor
    @return: The sensor object for this sensor
    """
    if sensor_name == 'withings_pulseo2':
        return WithingsPulseO2()


class Hub():
    def __init__(self):
        chdir('../../res')  # This is to access the res directory in hub
        self.config = ConfigParser.RawConfigParser()
        self.config.read('hub_config.txt')
        self.hub_id = self.config.get("id", "hub_id")
        self.sensors = []
        self.init_sensors()

    def init_sensors(self):
        """
        Initializes and connects to the sensors of this hub
        @return: A list of active sensors that can be interfaced with
        """
        print "Initializing sensors"
        for sensor in self.config.items('sensors'):
            self.sensors.append(get_sensor(*sensor))
            print "Initialized sensor: " + sensor[0] + "\n"
        # TODO try to connect to ble sensors

    def search_for_sensors(self):
        """
        Searches for sensors and returns a list of BLE sensors
        """
        print "(not really) Searching for sensors ...\nNo sensors found\n"
        # TODO: use gatttool lescan to search for BLE devices and return a list (or similar) of them.

    def add_sensor(self, name, mac_address):
        """
        Takes a mac adress and a name and adds it to the list of sensors of this hub
        @param mac_address: The mac address for the sensor
        @param name: The name of the sensor
        @return: True if sensor was successfully added to the list, false otherwise
        """
        print "Adding sensor: " + name + ", addr: " + mac_address
        if name not in self.sensors: # TODO this test never fails. comparing string with sensor object
            self.config.set('sensors', name, mac_address)
            config_file = open('hub_config.txt', 'w')
            self.config.write(config_file)
            config_file.close()
            self.sensors.append(get_sensor(name, mac_address))

    def get_sensors(self):
        """
        This function returns a list of the currently connected sensors
        @return:
        """
        print "sensors:" + str(self.sensors)
        return self.sensors

    def get_all_sensor_data(self):
        measurements = []
        end_time = dt.now()
        # TODO change this when we get caching to work
        start_time = end_time - timedelta(days=7)  # TODO should be 7 days
        for sensor in self.sensors:
            measurements += sensor.get_all_measurements(start_time, end_time)
        #for m in measurements:
        #    print m
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


def cache_data():
    caching.cache_measurements(hub.get_all_sensor_data())

program_functions = {'s': Hub.search_for_sensors,
                     'l': Hub.get_sensors,
                     'a': Hub.add_sensor,
                     'h': print_help,
                     'g': Hub.get_all_sensor_data,
                     'c': cache_data}
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
