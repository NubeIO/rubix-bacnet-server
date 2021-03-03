import logging

from registry.registry import RubixRegistry
from rubix_mqtt.mqtt import MqttClientBase

from src import MqttSetting
from src.utils import Singleton

logger = logging.getLogger(__name__)


def allow_only_on_prefix(func):
    def inner_function(*args, **kwargs):
        prefix_topic: str = MqttClient.prefix_topic()
        if not prefix_topic:
            return
        func(*args, **kwargs)

    return inner_function


class MqttClient(MqttClientBase, metaclass=Singleton):
    SEPARATOR: str = '/'

    @property
    def config(self) -> MqttSetting:
        return super().config if isinstance(super().config, MqttSetting) else MqttSetting()

    @allow_only_on_prefix
    def publish_value(self, topic_suffix: tuple, payload: str):
        if self.config.publish_value:
            self.__publish_mqtt_value(self.make_topic((self.config.topic,) + topic_suffix), payload)

    @allow_only_on_prefix
    def publish_debug(self, payload: str):
        if self.config.publish_debug:
            self.__publish_mqtt_value(self.make_topic((self.config.debug_topic,)), payload)

    def __publish_mqtt_value(self, topic: str, payload: str):
        if not self.status():
            logger.error(f"MQTT client {self.to_string()} is not connected...")
            return
        logger.debug(f"MQTT_PUBLISH: 'topic': {topic}, 'payload': {payload}, 'retain': {self.config.retain}")
        self.client.publish(topic, str(payload), qos=self.config.qos, retain=self.config.retain)

    @classmethod
    def prefix_topic(cls) -> str:
        wires_plat: dict = RubixRegistry().read_wires_plat()
        if not wires_plat:
            logger.error('Please add wires-plat on Rubix Service')
            return ''
        return MqttClient.SEPARATOR.join((wires_plat.get('client_id'), wires_plat.get('client_name'),
                                          wires_plat.get('site_id'), wires_plat.get('site_name'),
                                          wires_plat.get('device_id'), wires_plat.get('device_name')))

    def make_topic(self, parts: tuple) -> str:
        return MqttClient.SEPARATOR.join((self.prefix_topic(),) + parts)
