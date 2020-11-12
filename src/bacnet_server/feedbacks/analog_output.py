from bacpypes.local.object import AnalogOutputCmdObject
from bacpypes.primitivedata import Real

from src.bacnet_server.helpers.helper_point_array import create_object_identifier
from src.bacnet_server.helpers.helper_point_store import update_point_store
from src.bacnet_server.mqtt_connection import MqttConnection


class AnalogOutputFeedbackObject(AnalogOutputCmdObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._property_monitors["presentValue"].append(self.check_feedback)

    def check_feedback(self, old_value, new_value):
        update_point_store(self.objectName, new_value)
        object_identifier = create_object_identifier(self.objectIdentifier[0], self.objectIdentifier[1])
        present_value = self.presentValue
        if isinstance(present_value, Real):
            present_value = float(present_value.value)
        elif type(present_value) is float:
            present_value = float(present_value)
        topic = f"bacnet/server/points/ao/{object_identifier}"

        payload = str(present_value)
        print({'MQTT_PUBLISH': "MQTT_PUBLISH", 'topic': topic, 'payload': payload})
        print('MqttConnection.get_mqtt_client()', MqttConnection.get_mqtt_client())
        MqttConnection.get_mqtt_client().publish(topic, payload, qos=1, retain=True)
