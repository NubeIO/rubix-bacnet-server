import paho.mqtt.client as mqtt

from src.ini_config import config


class MqttConnection:
    __instance = None
    __client = None

    def __init__(self):
        if MqttConnection.__instance:
            raise Exception("MqttConnection class is a singleton class!")
        else:
            MqttConnection.__instance = self

    @staticmethod
    def get_instance():
        if MqttConnection.__instance is None:
            MqttConnection()
        return MqttConnection.__instance

    @staticmethod
    def get_mqtt_client():
        if MqttConnection.__instance is None:
            MqttConnection()
        return MqttConnection.__client

    @staticmethod
    def start():
        if MqttConnection.__instance is None:
            MqttConnection()
        MqttConnection.__client = mqtt.Client()
        MqttConnection.__client.loop_start()
        try:
            host = config.get('mqtt', 'host')
            port = int(config.get('mqtt', 'port'))
            MqttConnection.__client.connect(host, port, 60)
            MqttConnection.__client.loop_forever()
        except Exception as e:
            print(f"Error {e}")
