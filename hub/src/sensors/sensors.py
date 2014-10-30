from abc import ABCMeta, abstractmethod
from withings_pulseo2 import WithingsPulseO2


class Sensor():
    __metaclass__ = ABCMeta

    @property
    def name(self):
        raise NotImplementedError

    @property
    def last_updated(self):
        raise NotImplementedError

    @abstractmethod
    def get_all_measurements(self, start_time, end_time):
        """Retreive all measurements from start date to end date (including)"""
        return


def get_sensor(sensor_name, sensor_type, mac_address):
    """
    This is a factory that returns a sensor based on the sensor type

    @param sensor_name: The name of the sensor
    @param sensor_type: The type of the sensor
    @param mac_address: The MAC address of the sensor
    @return: The sensor object
    """
    if sensor_type == 'withings_pulseo2':
        return WithingsPulseO2(sensor_name)


class Measurement():
    def __init__(self, m_type, value, unit, date):
        self.m_type = m_type
        self.value = value
        self.unit = unit
        self.date = date

    def __repr__(self):
        return "Measurement at " + self.date.strftime('%Y-%m-%d') + ": type: " + str(self.m_type) + ", value:" + str(self.value)

