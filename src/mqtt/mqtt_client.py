import logging
import time

import paho.mqtt.client as mqtt_client

from src import MqttSetting
from src.utils import Singleton

logger = logging.getLogger(__name__)


class MqttClient(metaclass=Singleton):

    def __init__(self):
        self.__config = None
        self.__client = None

    @property
    def config(self) -> MqttSetting:
        return self.__config

    def status(self) -> bool:
        return self.__client.is_connected() if self.config and self.config.enabled and self.__client else False

    def start(self, config: MqttSetting):
        self.__config = config
        self.__client = mqtt_client.Client(self.config.name)
        if self.config.authentication:
            self.__client.username_pw_set(self.config.username, self.config.password)
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        if self.config.attempt_reconnect_on_unavailable:
            while True:
                try:
                    self.__client.connect(self.config.host, self.config.port, self.config.keepalive)
                    break
                except ConnectionRefusedError:
                    logger.error(
                        f'MQTT connection failure: ConnectionRefusedError. Attempting reconnect in '
                        f'{self.config.attempt_reconnect_secs} seconds')
                    time.sleep(self.config.attempt_reconnect_secs)
        else:
            try:
                self.__client.connect(self.config.host, self.config.port, self.config.keepalive)
            except Exception as e:
                self.__client = None
                logger.error(str(e))
                return
        self.__client.loop_forever()

    def get_topic(self, object_identifier, type_):
        return f"{self.config.topic}/{type_}/{object_identifier}"

    def publish_mqtt_value(self, topic, present_value):
        if not self.status():
            return
        retain = self.config.retain
        self.__client.publish(topic, str(present_value), qos=self.config.qos, retain=retain)

    def __on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code > 0:
            reasons = {
                1: 'Connection refused - incorrect protocol version',
                2: 'Connection refused - invalid client identifier',
                3: 'Connection refused - server unavailable',
                4: 'Connection refused - bad username or password',
                5: 'Connection refused - not authorised'
            }
            reason = reasons.get(reason_code, 'unknown')
            self.__client = None
            raise Exception(f'MQTT Connection Failure: {reason}')
        self.__client.subscribe(f'{self.config.topic}/#')

    def publish_debug(self, payload):
        self.publish_mqtt_value(self.config.debug_topic, payload)

    def __on_message(self, client, userdata, message):
        pass
