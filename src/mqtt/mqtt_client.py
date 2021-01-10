from logging import Logger

import paho.mqtt.client as mqtt_client
import time

from src import MqttSetting
from src.utils import Singleton


class MqttClient(metaclass=Singleton):

    def __init__(self):
        self.logger = None
        self.__config = None
        self.__client = None

    @property
    def config(self) -> MqttSetting:
        return self.__config

    def status(self) -> bool:
        return self.__client.is_connected() if self.config and self.config.enabled and self.__client else False

    def start(self, config: MqttSetting, logger: Logger):
        self.logger = logger or Logger(__name__)
        self.__config = config
        self.__client = mqtt_client.Client(self.config.name)
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        if self.config.attempt_reconnect_on_unavailable:
            while True:
                try:
                    self.__client.connect(self.config.host, self.config.port, self.config.keepalive)
                    break
                except ConnectionRefusedError:
                    self.logger.error(
                        f'MQTT connection failure: ConnectionRefusedError. Attempting reconnect in '
                        f'{self.config.attempt_reconnect_secs} seconds')
                    time.sleep(self.config.attempt_reconnect_secs)
        else:
            try:
                self.__client.connect(self.config.host, self.config.port, self.config.keepalive)
            except Exception as e:
                self.__client = None
                self.logger.error(str(e))
                return
        self.__client.loop_forever()

    def publish_mqtt_value(self, object_identifier, present_value):
        topic = f"rubix/bacnet/server/points/ao/{object_identifier}"
        retain = self.config.retain
        if not self.status():
            self.logger.error("MQTT is not connected...")
            self.logger.error(
                f"Failed MQTT_PUBLISH: {{'topic': {topic}, 'payload': {present_value}, 'retain': {retain}}}")
            return
        self.logger.debug(f"MQTT_PUBLISH: {{'topic': {topic}, 'payload': {present_value}, 'retain': {retain}}}")
        self.__client.publish(topic, present_value, qos=1, retain=retain)

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

    def __on_message(self, client, userdata, message):
        pass
