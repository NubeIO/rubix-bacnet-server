import json
import os
from abc import ABC

from flask import Flask
from mrb.setting import MqttSetting as MqttRestBridgeSetting
from rubix_mqtt.setting import MqttSettingBase


class BaseSetting(ABC):

    def reload(self, setting: dict):
        if setting is not None:
            self.__dict__ = {k: setting.get(k, v) for k, v in self.__dict__.items()}
        return self

    def serialize(self, pretty=True) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, indent=2 if pretty else None)

    def to_dict(self):
        return json.loads(self.serialize(pretty=False))


class BACnetSetting(BaseSetting):
    KEY = 'bacnet'

    def __init__(self):
        self.enabled: bool = True
        self.master_enabled: bool = True
        self.ip = '192.168.0.100'
        self.port = 47808
        self.device_id = 123
        self.local_obj_name = 'Nube-IO'
        self.model_name = 'rubix-bac-stack-RC4'
        self.vendor_id = 1173
        self.vendor_name = 'Nube iO Operations Pty Ltd'
        self.attempt_reconnect_secs = 5


class MqttSetting(MqttSettingBase):
    KEY = 'mqtt'

    def __init__(self):
        super().__init__()
        self.name = 'bacnet-server-mqtt'
        self.publish_value = True
        self.topic = 'rubix/bacnet_server/points'
        self.publish_debug = True
        self.debug_topic = 'rubix/bacnet_server/debug'


class AppSetting:
    PORT: int = 1717
    GLOBAL_DIR_ENV = 'RUBIX_BACNET_GLOBAL'
    DATA_DIR_ENV = 'RUBIX_BACNET_DATA'
    CONFIG_DIR_ENV = 'RUBIX_BACNET_CONFIG'
    FLASK_KEY: str = 'APP_SETTING'
    default_global_dir: str = 'out'
    default_data_dir: str = 'data'
    default_config_dir: str = 'config'
    default_identifier: str = 'bacnet'
    default_setting_file: str = 'config.json'
    default_logging_conf: str = 'logging.conf'
    fallback_logging_conf: str = 'config/logging.example.conf'
    fallback_prod_logging_conf: str = 'config/logging.prod.example.conf'

    def __init__(self, **kwargs):
        self.__port = kwargs.get('port') or AppSetting.PORT
        self.__global_dir = self.__compute_dir(kwargs.get('global_dir'), AppSetting.default_global_dir, 0o777)
        self.__data_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('data_dir')),
                                             self.__join_global_dir(AppSetting.default_data_dir))
        self.__config_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('config_dir')),
                                               self.__join_global_dir(AppSetting.default_config_dir))
        self.__identifier = kwargs.get('identifier') or AppSetting.default_identifier
        self.__prod = kwargs.get('prod') or False
        self.__mqtt_setting = MqttSetting()
        self.__bacnet_setting = BACnetSetting()
        self.__mqtt_rest_bridge_setting = MqttRestBridgeSetting()

    @property
    def port(self):
        return self.__port

    @property
    def global_dir(self):
        return self.__global_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def config_dir(self):
        return self.__config_dir

    @property
    def identifier(self):
        return self.__identifier

    @property
    def prod(self) -> bool:
        return self.__prod

    @property
    def mqtt(self) -> MqttSetting:
        return self.__mqtt_setting

    @property
    def bacnet(self) -> BACnetSetting:
        return self.__bacnet_setting

    @property
    def mqtt_rest_bridge_setting(self) -> MqttRestBridgeSetting:
        return self.__mqtt_rest_bridge_setting

    def serialize(self, pretty=True) -> str:
        m = {BACnetSetting.KEY: self.bacnet, MqttSetting.KEY: self.mqtt, 'prod': self.prod,
             'global_dir': self.global_dir, 'data_dir': self.data_dir, 'config_dir': self.config_dir}
        return json.dumps(m, default=lambda o: o.to_dict() if isinstance(o, BaseSetting) else o.__dict__,
                          indent=2 if pretty else None)

    def reload(self, setting_file: str, is_json_str: bool = False):
        data = self.__read_file(setting_file, self.__config_dir, is_json_str)
        self.__mqtt_setting = self.__mqtt_setting.reload(data.get(MqttSetting.KEY))
        self.__bacnet_setting = self.__bacnet_setting.reload(data.get(BACnetSetting.KEY))
        self.__mqtt_rest_bridge_setting = self.__mqtt_rest_bridge_setting.reload(data.get('mqtt_rest_bridge_listener'))
        self.__mqtt_rest_bridge_setting.name = 'bacnet_mqtt_rest_bridge_listener'
        return self

    def init_app(self, app: Flask):
        app.config[AppSetting.FLASK_KEY] = self
        return self

    def __join_global_dir(self, _dir):
        return _dir if _dir is None or _dir.strip() == '' else os.path.join(self.__global_dir, _dir)

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d

    @staticmethod
    def __read_file(setting_file: str, _dir: str, is_json_str=False):
        if is_json_str:
            return json.loads(setting_file)
        if setting_file is None or setting_file.strip() == '':
            return {}
        s = setting_file if os.path.isabs(setting_file) else os.path.join(_dir, setting_file)
        if not os.path.isfile(s) or not os.path.exists(s):
            return {}
        with open(s) as json_file:
            return json.load(json_file)
