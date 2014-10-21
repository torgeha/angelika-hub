from withings_pulseo2 import WithingsPulseO2
from datetime import datetime as dt, timedelta

sensor = WithingsPulseO2()
end_date = dt.now()
start_date = end_date - timedelta(days=30)
measurements = sensor.get_all_measurements(start_date, end_date)
for m in measurements:
    print m