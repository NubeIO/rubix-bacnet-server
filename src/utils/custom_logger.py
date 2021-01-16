import logging

from src.mqtt import MqttClient


class CustomLogger(logging.Logger):
    def handle(self, record):
        if MqttClient().config and MqttClient().config.publish_debug:
            MqttClient().publish_debug(record.msg)
        super().handle(record)
