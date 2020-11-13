from flask_restful import Resource
from datetime import datetime
import time

startTime = time.time()
up_time_date = str(datetime.now())


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - startTime


class Ping(Resource):
    def get(self):
        up_time = get_up_time()
        up_min = up_time / 60
        up_min = round(up_min, 2)
        up_min = str(up_min)
        up_hour = up_time / 3600
        up_hour = round(up_hour, 2)
        up_hour = str(up_hour)
        return {'up_time_date': up_time_date, 'up_min': up_min, 'up_hour': up_hour}
