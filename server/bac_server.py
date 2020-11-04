import time
from bacpypes.basetypes import EngineeringUnits
from bacpypes.local.object import AnalogOutputCmdObject, BinaryOutputCmdObject
from bacpypes.primitivedata import CharacterString


from server.bac_class import BAC0_Device
from server.breakdowns.helper_point_array import default_values, create_object_identifier
from server.breakdowns.point_save_on_change import point_save

from tinydb import TinyDB, Query

from server.config import PointConfig, NetworkConfig, DbConfig

global bacnet
db_location = DbConfig.location
db_name = DbConfig.name
db_file = f"{db_location}/{db_name}.json"
db = TinyDB(db_file)
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


def start():
    global bacnet
    ao_count = PointConfig.ao_count
    bo_count = PointConfig.bo_count

    ip = NetworkConfig.ip
    port = NetworkConfig.port
    device_id = NetworkConfig.deviceId
    local_obj_name = NetworkConfig.localObjName

    bacnet = BAC0_Device(ip, device_id, local_obj_name)
    bacnet.start_device(port)
    for i in range(1, int(bo_count) + 1):
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
    for i in range(1, int(ao_count) + 1):
        default_pv = 0.0
        object_type = 'analogOutput'
        [priority_array, present_value] = default_values(object_type, i, default_pv, db, Points)
        ao = AnalogOutputFeedbackObject(
            objectIdentifier=(object_type, i),
            objectName='analogOutput-%d' % (i,),
            presentValue=present_value,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            relinquishDefault=0.0,
            priorityArray=priority_array,
            units=EngineeringUnits("milliseconds"),
            description=CharacterString("Sets fade time between led colors (0-32767)"),
        )
        bacnet.device.this_application.add_object(ao)
    while True:
        time.sleep(0.2)


if __name__ == '__main__':
    start()
