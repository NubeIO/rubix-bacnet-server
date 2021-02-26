from bacpypes.local.object import AnalogOutputCmdObject
from bacpypes.primitivedata import Real
from flask import current_app

from src.bacnet_server.helpers.helper_point_array import create_object_identifier, serialize_priority_array
from src.bacnet_server.helpers.helper_point_store import update_point_store
from src.bacnet_server.models.model_priority_array import PriorityArrayModel
from src.mqtt import MqttClient


class AnalogOutputFeedbackObject(AnalogOutputCmdObject):
    def __init__(self, **kwargs):
        self.__app_context = current_app.app_context
        super().__init__(**kwargs)
        self._property_monitors["presentValue"].append(self.check_feedback)

    def check_feedback(self, old_value, new_value):
        priority_array = self._dict_contents().get('priorityArray')
        serialized_priority_array = serialize_priority_array(priority_array)
        with self.__app_context():
            PriorityArrayModel.filter_by_point_uuid(self.profileName).update(serialized_priority_array)
            update_point_store(self.profileName, new_value)
            object_identifier = create_object_identifier(self.objectIdentifier[0], self.objectIdentifier[1])
            present_value = self.presentValue
            if isinstance(present_value, Real):
                present_value = float(present_value.value)
            elif type(present_value) is float:
                present_value = float(present_value)
            mqtt_client = MqttClient()
            mqtt_client.publish_value(('ao', object_identifier), present_value)
