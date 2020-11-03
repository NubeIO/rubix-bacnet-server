import time
import BAC0
from bacpypes.basetypes import EngineeringUnits
from bacpypes.local.object import AnalogOutputCmdObject, BinaryOutputCmdObject
from bacpypes.primitivedata import CharacterString
from tinydb import TinyDB, Query

from server_v2.breakdowns.helper_point_array import default_values
from server_v2.breakdowns.point_save_on_change import point_save
from tests.test_working import create_object_identifier

global bacnet
db = TinyDB('points.json')
Points = Query()


# @register_object_type(vendor_id=999)
class BinaryOutputFeedbackObject(BinaryOutputCmdObject):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._property_monitors["presentValue"].append(self.check_feedback)

    def check_feedback(self, old_value, new_value):
        pnt_dict = self._dict_contents()
        object_identifier = create_object_identifier(self.objectIdentifier)
        object_name = self.objectName
        object_type = self.objectType
        present_value = self.presentValue
        _type = "enumerated"
        point_save(pnt_dict, object_identifier, object_name, object_type,
                   present_value, _type, old_value, new_value, db, Points)


class AnalogOutputFeedbackObject(AnalogOutputCmdObject):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._property_monitors["presentValue"].append(self.check_feedback)

    def check_feedback(self, old_value, new_value):
        pnt_dict = self._dict_contents()
        object_identifier = create_object_identifier(self.objectIdentifier)
        object_name = self.objectName
        object_type = self.objectType
        present_value = self.presentValue
        _type = "real"
        point_save(pnt_dict, object_identifier, object_name, object_type,
                   present_value, _type, old_value, new_value, db, Points)


class BAC0_Converter:
    def __init__(self, ip, instance_number, obj_name):
        self.ip = ip
        self.instance_number = instance_number
        self.obj_name = obj_name

    def start_device(self, init_port):
        self.device = BAC0.lite(
            ip=self.ip,
            deviceId=self.instance_number,
            localObjName=self.obj_name,
            port=init_port
        )


RANDOM_OBJECT_COUNT = 1


def start():
    global bacnet
    bacnet = BAC0_Converter('192.168.0.101/24', 123, 'Pi')
    bacnet.start_device(47808)
    for i in range(1, RANDOM_OBJECT_COUNT + 1):
        default_pv = 'inactive'
        object_type = 'binaryOutput'
        [priority_array, present_value] = default_values(object_type, i, default_pv, db, Points)
        bo = BinaryOutputFeedbackObject(
            objectIdentifier=(object_type, i),
            objectName='binaryOutput-%d' % (i,),
            presentValue=present_value,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            feedbackValue="inactive",
            relinquishDefault="inactive",
            priorityArray=priority_array,
            description=CharacterString("Sets fade time between led colors (0-32767)"),
        )
        bacnet.device.this_application.add_object(bo)
    for i in range(1, RANDOM_OBJECT_COUNT + 1):
        default_pv = 0.0
        object_type = 'analogOutput'
        [priority_array, present_value] = default_values(object_type, i, default_pv, db, Points)
        ao = AnalogOutputFeedbackObject(
            objectIdentifier=(object_type, i),
            objectName='analogOutput-%d' % (i,),
            presentValue=present_value,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            relinquishDefault=22.2,
            priorityArray=priority_array,
            units=EngineeringUnits("milliseconds"),
            description=CharacterString("Sets fade time between led colors (0-32767)"),
        )
        bacnet.device.this_application.add_object(ao)
    while True:
        time.sleep(0.2)


if __name__ == '__main__':
    start()
