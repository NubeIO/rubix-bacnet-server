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
        if not MqttConnection.__instance:
            MqttConnection.__instance = MqttConnection()
        return MqttConnection.__client

    def start(self):
        self.__client = mqtt.Client()
        self.__client.loop_start()
        try:
            self.__client.connect("0.0.0.0", 1883, 60)
            self.__client.loop_forever()
        except Exception as e:
            print(f"Error {e}")
