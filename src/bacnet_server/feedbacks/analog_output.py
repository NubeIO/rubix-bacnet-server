from bacpypes.local.object import AnalogOutputCmdObject
from bacpypes.primitivedata import Real

from src.bacnet_server.helpers.helper_point_array import create_object_identifier, serialize_priority_array
from src.bacnet_server.helpers.helper_point_store import update_point_store
from src.bacnet_server.models.model_priority_array import PriorityArrayModel
from src.bacnet_server.mqtt_client import MqttClient
from src.ini_config import mqtt__publish_value


class AnalogOutputFeedbackObject(AnalogOutputCmdObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._property_monitors["presentValue"].append(self.check_feedback)

    def check_feedback(self, old_value, new_value):
        priority_array = self._dict_contents().get('priorityArray')
        serialized_priority_array = serialize_priority_array(priority_array)
        PriorityArrayModel.filter_by_point_uuid(self.profileName).update(serialized_priority_array)
        update_point_store(self.profileName, new_value)
        object_identifier = create_object_identifier(self.objectIdentifier[0], self.objectIdentifier[1])
        present_value = self.presentValue
        if isinstance(present_value, Real):
            present_value = float(present_value.value)
        elif type(present_value) is float:
            present_value = float(present_value)
        if mqtt__publish_value:
            MqttClient.publish_mqtt_value(object_identifier, present_value)
