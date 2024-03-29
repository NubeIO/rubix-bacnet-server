import time
from datetime import datetime

from flask import current_app
from rubix_http.resource import RubixResource

from src.bacnet_server import BACServer
from src.mqtt import MqttClient
from src.utils.project import get_version

start_time = time.time()
up_time_date = str(datetime.now())


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - start_time


class Ping(RubixResource):
    @classmethod
    def get(cls):
        up_time = get_up_time()
        up_min = up_time / 60
        up_min = "{:.2f}".format(up_min)
        up_hour = up_time / 3600
        up_hour = "{:.2f}".format(up_hour)
        from src import AppSetting
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        deployment_mode = 'production' if setting.prod else 'development'

        return {
            'version': get_version(),
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            'deployment_mode': deployment_mode,
            'bacnet': {
                'enabled': setting.bacnet.enabled,
                'status': BACServer().status(),
                'use_pre_set_ethernet_interface': setting.bacnet.enable_ip_by_nic_name,
                'pre_set_ethernet_interface': setting.bacnet.ip_by_nic_name,
                'default_point_cov': setting.bacnet.default_point_cov
            },
            'mqtt': {
                'enabled': setting.mqtt.enabled,
                'status': MqttClient().status()
            }
        }
