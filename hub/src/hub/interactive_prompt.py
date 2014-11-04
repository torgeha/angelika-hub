import inspect
from hub import Hub
from traceback import format_exc

__author__ = 'David'
__version__ = '0.0.1'


def user_input():
    raw_program_input = raw_input("angelika_hub_" + __version__ + "> ")
    if raw_program_input == "" or raw_program_input == "exit":
        return False
    program_input = str.split(raw_program_input, " ", 1)
    program_function = program_functions.get(program_input[0])
    if not program_function:
        print "No such function\n"
        print_help()
        return True
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
    return True


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


def main():
    while user_input():
        pass


if __name__ == 'main':
    program_functions = {'s': Hub.search_for_sensors,
                         'l': Hub.get_sensors,
                         'a': Hub.add_sensor,
                         'h': print_help,
                         'g': Hub.get_all_sensor_data}
    hub = Hub()
    main()