from abc import ABCMeta, abstractmethod


class Sensor():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_measurements(self, start_date, end_date):
        """Retreive all measurements from start date to end date (including)"""
        return


class Measurement():
    def __init__(self, m_type, value, unit, date):
        self.m_type = m_type
        self.value = value
        self.unit = unit
        self.date = date

    def __repr__(self):
        return "Measurement at " + self.date.strftime('%Y-%m-%d') + ": type: " + str(self.m_type) + ", value:" + str(self.value)
