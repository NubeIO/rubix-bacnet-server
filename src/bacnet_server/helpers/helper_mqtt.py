import logging

from src.bacnet_server.mqtt_connection import MqttConnection

logger = logging.getLogger(__name__)


def publish_mqtt_value(object_identifier, present_value):
    topic = f"bacnet/server/points/ao/{object_identifier}"

    logging.info({'MQTT_PUBLISH': "MQTT_PUBLISH", 'topic': topic, 'payload': present_value})
    MqttConnection.get_mqtt_client().publish(topic, present_value, qos=1, retain=True)
