
# sys.path.insert(0, '../sensors')
# from withings_pulseo2 import WithingsPulseO2
# from withings_pulseo2 import WithingsPulseO2
# from src import sensors
from sensors.withings_pulseo2 import WithingsPulseO2


class SensorFactory:

    def get_sensor_instance(self, sensor_name, config):
        """
        Takes a name to create a new sensor
        The sensor to be created depends on type of sensor, and it must subclass the sensor class
        @param sensor_name: The name of the sensor
        @return: The sensor object for this sensor
        """
        sensor_type = config.get(sensor_name, 'type')
        mac_address = config.get(sensor_name, 'mac_address')
        if sensor_type == 'withings_pulseo2':
            sensor = WithingsPulseO2(sensor_name)
        sensor.last_updated = config.getint(sensor_name, 'last_update')
        return sensor
