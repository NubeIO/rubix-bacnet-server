import paho.mqtt.client as mqtt


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
            # TODO add mqtt data to the ini file
            MqttConnection.__client.connect("0.0.0.0", 1883, 60)
            MqttConnection.__client.loop_forever()
        except Exception as e:
            print(f"Error {e}")
