import os
import time
from datetime import datetime

from flask_restful import Resource

from src.bacnet_server.bac_server import BACServer
from src.bacnet_server.mqtt_client import MqttClient
from src.ini_config import settings__enable_mqtt, settings__enable_bacnet_server

start_time = time.time()
up_time_date = str(datetime.now())


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - start_time


class Ping(Resource):
    def get(self):
        up_time = get_up_time()
        up_min = up_time / 60
        up_min = "{:.2f}".format(up_min)
        up_hour = up_time / 3600
        up_hour = "{:.2f}".format(up_hour)
        deployment_mode = 'production' if os.environ.get("data_dir") is not None else 'development'

        return {
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            'deployment_mode': deployment_mode,
            'mqtt_client_status': MqttClient.get_instance().status(),
            'bacnet_server_status': BACServer.get_instance().status(),
            'settings': {
                'enable_mqtt': settings__enable_mqtt,
                'enable_bacnet_server': settings__enable_bacnet_server,
            },
        }
