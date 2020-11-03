import os
import time
import BAC0
from bacpypes.basetypes import PriorityArray, PriorityValue, EngineeringUnits
from bacpypes.local.object import AnalogOutputCmdObject, BinaryOutputCmdObject
from bacpypes.object import register_object_type
from bacpypes.primitivedata import CharacterString
from tinydb import TinyDB, Query

global bacnet
db = TinyDB('points.json')
Points = Query()
_debug = True


def create_object_identifier(obj):
    return "-".join(str(v) for v in obj)


def highest_priority(iterable, _type, default=None):
    if iterable:
        priority = 0
        for value in iterable:
            priority += 1
            val = value.get(_type)
            if val is not None:
                return [val, priority]
    return default


def point_save(pnt_dict, object_identifier, object_name, object_type,
               present_value, _type, old_value, new_value):
    _priority_array = pnt_dict.get("priorityArray")
    highest_priority_array = highest_priority(_priority_array, _type)
    priority_value = None
    priority_pri_value = None
    if highest_priority_array is not None:
        priority_value = highest_priority_array[0]
        priority_pri_value = highest_priority_array[1]
    else:
        priority_value = priority_value
        priority_pri_value = priority_pri_value

    if _debug:
        print({"object_identifier": object_identifier,
               "object_name": object_name,
               "object_type": object_type,
               "_priority_array": _priority_array,
               "priority_value": priority_value,
               "priority_pri_value": priority_pri_value,
               "present_value": present_value, 'old_value': old_value,
               'new_value': new_value})

    insert_if_none = db.search(Points.object_identifier == object_identifier)
    if not insert_if_none:
        db.insert({"object_identifier": object_identifier,
                   "object_name": object_name,
                   "object_type": object_type,
                   "_priority_array": _priority_array,
                   "highest_priority_array": highest_priority_array,
                   "priority_value": priority_value,
                   "priority_pri_value": priority_pri_value,
                   "present_value": present_value})
    else:
        db.update({
            "_priority_array": _priority_array,
            "highest_priority_array": highest_priority_array,
            "priority_value": priority_value,
            "priority_pri_value": priority_pri_value,
            "present_value": present_value,
        }, Points.object_identifier == object_identifier)


@register_object_type(vendor_id=999)
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
                   present_value, _type, old_value, new_value)


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
                   present_value, _type, old_value, new_value)


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
        [priority_array, present_value] = get_priority_array_and_present_value('binaryOutput', i)
        if priority_array is None:
            priority_array = PriorityArray(),
        if present_value is None:
            present_value = "inactive",
        bo = BinaryOutputFeedbackObject(
            objectIdentifier=('binaryOutput', i),
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
        [priority_array, present_value] = get_priority_array_and_present_value('analogOutput', i)
        if priority_array is None:
            priority_array = PriorityArray(),
        if present_value is None:
            present_value = 1.0,
        ao = AnalogOutputFeedbackObject(
            objectIdentifier=('analogOutput', i),
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


def get_priority_array_and_present_value(identifier, i):
    point = db.search(Points.object_identifier == create_object_identifier((identifier, i)))
    priority_array = PriorityArray()
    present_value = 'inactive'
    if point and len(point) and point[0].get('_priority_array'):
        # convert `[{"null": []}, ...` to `[{"null": ()}, ...`
        _priority_array = point[0].get('_priority_array')
        _priority_array_temp = map(lambda x: {'null': ()} if 'null' in x.keys() else x, _priority_array)
        _priority_array = list(_priority_array_temp)
        for j in range(16):
            priority_array.__setitem__(j + 1, PriorityValue(**_priority_array[j]))
    if point and len(point) and point[0].get('present_value'):
        present_value = point[0].get('present_value')
    return [priority_array, present_value]


if __name__ == '__main__':
    start()
