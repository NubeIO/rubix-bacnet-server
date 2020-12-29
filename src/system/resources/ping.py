from datetime import datetime

import time
from flask import current_app
from flask_restful import Resource

from src.bacnet_server import BACServer
from src.mqtt import MqttClient

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
        from src import AppSetting
        setting: AppSetting = current_app.config[AppSetting.KEY]
        deployment_mode = 'production' if setting.prod else 'development'

        mqttc = MqttClient()
        bac_server = BACServer()
        return {
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            'deployment_mode': deployment_mode,
            'mqtt_client_status': mqttc.status(),
            'bacnet_server_status': bac_server.status(),
            'settings': {
                'enable_mqtt': mqttc.config.enabled,
                'enable_bacnet_server': bac_server.config.enabled,
            },
        }
