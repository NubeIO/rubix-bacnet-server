from flask_restful import Resource
from datetime import datetime
import time

startTime = time.time()
up_time_date = str(datetime.now())


def getUptime():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - startTime


class Ping(Resource):
    def get(self):
        now = datetime.now()
        now = str(now)
        up_time = getUptime()
        up_min = up_time / 60
        up_hour = up_time / 3600
        up_min = str(up_min)
        up_hour = str(up_hour)
        return {'ping': True, 'now': now, 'up_time_date': up_time_date, 'up_min': up_min, 'up_hour': up_hour}
