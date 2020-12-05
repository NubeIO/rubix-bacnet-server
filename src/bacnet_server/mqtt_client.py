import logging
import time

import paho.mqtt.client as mqtt_client

from src.ini_config import *

MQTT_CLIENT_NAME = 'bacnet-server-mqtt'
MQTT_TOPIC = 'rubix/points'

logger = logging.getLogger(__name__)


class MqttClient:
    __instance = None
    __client = None

    def __init__(self):
        if MqttClient.__instance:
            raise Exception("MqttConnection class is a singleton class!")
        else:
            MqttClient.__instance = self

    @staticmethod
    def get_instance():
        if MqttClient.__instance is None:
            MqttClient()
        return MqttClient.__instance

    def status(self) -> bool:
        if not MqttClient.__client:
            return False
        else:
            return MqttClient.__client.is_connected()

    def start(self):
        MqttClient.__client = mqtt_client.Client(MQTT_CLIENT_NAME)
        MqttClient.__client.on_connect = MqttClient.__on_connect
        MqttClient.__client.on_message = MqttClient.__on_message
        if mqtt__attempt_reconnect_on_unavailable:
            while True:
                try:
                    MqttClient.__client.connect(mqtt__host, mqtt__port, mqtt__keepalive)
                    break
                except ConnectionRefusedError:
                    if mqtt__debug:
                        logger.error(
                            f'MQTT connection failure: ConnectionRefusedError. Attempting reconnect in '
                            f'{mqtt__attempt_reconnect_secs} seconds')
                    time.sleep(mqtt__attempt_reconnect_secs)
        else:
            try:
                MqttClient.__client.connect(mqtt__host, mqtt__port, mqtt__keepalive)
            except Exception as e:
                MqttClient.__client = None
                logger.error(str(e))
                return
        MqttClient.__client.loop_forever()

    @staticmethod
    def publish_mqtt_value(object_identifier, present_value):
        topic = f"bacnet/server/points/ao/{object_identifier}"
        retain = mqtt__retain
        if not MqttClient.get_instance().status():
            logger.error("MQTT is not connected...")
            logging.error(f"Failed MQTT_PUBLISH: {{'topic': {topic}, 'payload': {present_value}, 'retain': {retain}}}")
            return
        if mqtt__debug:
            logging.info(f"MQTT_PUBLISH: {{'topic': {topic}, 'payload': {present_value}, 'retain': {retain}}}")
        MqttClient.__client.publish(topic, present_value, qos=1, retain=retain)

    @staticmethod
    def __on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code > 0:
            reasons = {
                1: 'Connection refused - incorrect protocol version',
                2: 'Connection refused - invalid client identifier',
                3: 'Connection refused - server unavailable',
                4: 'Connection refused - bad username or password',
                5: 'Connection refused - not authorised'
            }
            reason = reasons.get(reason_code, 'unknown')
            MqttClient.__client = None
            raise Exception(f'MQTT Connection Failure: {reason}')
        MqttClient.__client.subscribe(f'{MQTT_TOPIC}/#')

    @staticmethod
    def __on_message(client, userdata, message):
        pass
