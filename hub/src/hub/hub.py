from inspect import getargspec
from traceback import format_exc


__author__ = 'David'
__version__ = "0.0.1"


def init_sensors():
    """
    Initializes and connects to the sensors of this hub
    @return: A list of active sensors that can be interfaced with
    """
    print "Initializing sensors\n"
    # TODO: Make some sort of txt or config file with the sensors this hub should be connected to.
    # TODO: Check if a config file exist and try to connect to the sensors.
    # Not sure if we should use the sensor class, and have a list of sensors
    # or if we should use just a list of mac addresses.
    # The config file will just have the mac addresses though.


def search_for_sensors():
    """
    Searches for sensors and returns a list of BLE sensors
    """
    print "Searching for sensors ...\nNo sensors found\n"
    # TODO: use gatttool lescan to search for BLE devices and return a list (or similar) of them.


def add_sensor(mac_address, name):
    """
    @param mac_address: The mac address for the sensor
    @param name: The name of the sensor
    Takes a mac adress and a name and adds it to the list of sensors of this hub
    @return: True if sensor was successfully added to the list, false otherwise
    """
    print "Adding sensor: " + name + ", addr: " + mac_address
    # TODO: add sensor to list and write to file.


def get_sensors():
    """
    This function returns a list of the currently
    @return:
    """
    print "sensors: None"


def print_help():
    """
    Prints what functions are allowed to use
    """
    print "Usage: action [arguments]: function"
    for k, v in program_functions.iteritems():
        print k + " " + str(getargspec(v).args) + ": " + v.__name__


program_functions = {'s': search_for_sensors,
                     'l': get_sensors,
                     'a': add_sensor,
                     'h': print_help}


def main():
    """
    The main method of the hub. This is where the magic happens
    """
    init_sensors()
    while True:
        raw_program_input = raw_input("angelika_hub_" + __version__ + "> ")
        if raw_program_input == "" or raw_program_input == "exit":
            break
        program_input = str.split(raw_program_input, " ", 1)
        program_function = program_functions.get(program_input[0])
        try:
            if len(program_input) > 1:
                arguments = str.split(program_input[1])
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

















