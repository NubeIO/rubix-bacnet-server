import json
import logging
from typing import Union

from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info
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
    def publish_value(self, topic_suffix: tuple, value: str, priority: int):
        if self.config.publish_value:
            output = {
                'value': value,
                'priority': priority
            }
            payload = json.dumps(output)
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
        device_info: Union[DeviceInfoModel, None] = get_device_info()
        if not device_info:
            logger.error('Please add device-info on Rubix Service')
            return ''
        return MqttClient.SEPARATOR.join((device_info.client_id, device_info.client_name,
                                          device_info.site_id, device_info.site_name,
                                          device_info.device_id, device_info.device_name))

    def make_topic(self, parts: tuple) -> str:
        return MqttClient.SEPARATOR.join((self.prefix_topic(),) + parts)
