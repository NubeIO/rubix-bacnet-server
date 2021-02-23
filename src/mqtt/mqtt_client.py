import logging

from rubix_mqtt.mqtt import MqttClientBase

from src import MqttSetting
from src.utils import Singleton

logger = logging.getLogger(__name__)


class MqttClient(MqttClientBase, metaclass=Singleton):

    @property
    def config(self) -> MqttSetting:
        return super().config

    def get_topic(self, object_identifier, type_):
        return f"{self.config.topic}/{type_}/{object_identifier}"

    def publish_mqtt_value(self, topic, present_value):
        if not self.status():
            logger.error(f"MQTT client {self.to_string()} is not connected...")
            return
        retain = self.config.retain
        self.client.publish(topic, str(present_value), qos=self.config.qos, retain=retain)

    def publish_debug(self, payload):
        self.publish_mqtt_value(self.config.debug_topic, payload)
