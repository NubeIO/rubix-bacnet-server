from logging import StreamHandler


class MqttStreamHandler(StreamHandler):

    def emit(self, record):
        from src.mqtt import MqttClient

        if MqttClient().config and MqttClient().config.publish_debug:
            try:
                msg = self.format(record)
                MqttClient().publish_debug(msg)
            except Exception as e:
                MqttClient().publish_debug(str(e))
