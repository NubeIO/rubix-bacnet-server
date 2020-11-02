import os
import time
import BAC0
from bacpypes.basetypes import PriorityArray, PriorityValue
from bacpypes.local.object import AnalogValueCmdObject, BinaryOutputCmdObject
from bacpypes.object import register_object_type
from tinydb import TinyDB, Query

global bacnet
db = TinyDB('points.json')
Points = Query()


def create_object_identifier(obj):
    return "-".join(str(v) for v in obj)


@register_object_type(vendor_id=999)
class BinaryOutputFeedbackObject(BinaryOutputCmdObject):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        # listen for changes to the present value
        self._property_monitors["presentValue"].append(self.check_feedbacks)

    def check_feedbacks(self, old_value, new_value):
        print(
            "check_feedback %r %r", old_value, new_value
        )

        def highest_priority(iterable, default=None):
            if iterable:
                _count = 0
                for item in iterable:
                    _count += 1
                    if item.get('enumerated') == 0 or item.get('enumerated') == 1:
                        return {"value": item, "priority": _count}
            return default

        pnt_dict = self._dict_contents()
        print(pnt_dict)
        _priority_array = pnt_dict.get("priorityArray")
        print(_priority_array)
        highest_priority_array = highest_priority(_priority_array)
        object_identifier = create_object_identifier(self.objectIdentifier)
        object_name = self.objectName
        object_type = self.objectType
        present_value = self.presentValue
        priority_pri_value = highest_priority_array.get("value", {}).get('enumerated')
        priority_value = highest_priority_array.get("priority")
        print({"object_identifier": object_identifier,
               "object_name": object_name,
               "object_type": object_type,
               "_priority_array": _priority_array,
               "priority_value": priority_value,
               "priority_pri_value": priority_pri_value,
               "present_value": present_value})
        if new_value == present_value:
            insert_if_none = db.search(Points.object_identifier == object_identifier)
            print('insert_if_none', insert_if_none)
            if not insert_if_none:  # first run
                db.insert({"object_identifier": object_identifier,
                           "object_name": object_name,
                           "object_type": object_type,
                           "_priority_array": _priority_array,
                           "priority_value": priority_value,
                           "priority_pri_value": priority_pri_value,
                           "present_value": present_value})
            else:
                if new_value == 1:
                    self.presentValue = "active"
                elif new_value == 0:
                    self.presentValue = "inactive"
                db.update({
                    "_priority_array": _priority_array,
                    "priority_value": priority_value,
                    "priority_pri_value": priority_pri_value,
                    "present_value": present_value,
                }, Points.object_identifier == object_identifier)


class AnalogOutputFeedbackObject(AnalogValueCmdObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # listen for changes to the present value
        self._property_monitors["presentValue"].append(self.check_feedbacks)

    def check_feedbacks(self, old_value, new_value):
        print(
            "check_feedback %r %r", old_value, new_value
        )
        if new_value == self.presentValue:
            print(1111111)
            # self.eventState = "normal"
            # self.statusFlags["inAlarm"] = False
        else:
            print(222222)
            # self.eventState = "offnormal"
            # self.statusFlags["inAlarm"] = True


RANDOM_OBJECT_COUNT = int(os.getenv('RANDOM_OBJECT_COUNT', 5))


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


def start():
    global bacnet
    bacnet = BAC0_Converter('192.168.0.101/24', 123, 'Pi')
    bacnet.start_device(47808)
    for i in range(1, RANDOM_OBJECT_COUNT + 1):
        [priority_array, present_value] = get_priority_array_and_present_value('binaryOutput', i)
        ravo = BinaryOutputFeedbackObject(
            objectIdentifier=('binaryOutput', i),
            objectName='binaryOutput-%d' % (i,),
            presentValue=present_value,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            feedbackValue="inactive",
            relinquishDefault="inactive",
            priorityArray=priority_array,
        )
        bacnet.device.this_application.add_object(ravo)
    for i in range(1, RANDOM_OBJECT_COUNT + 1):
        [priority_array, _] = get_priority_array_and_present_value('analogValue', i)
        ravo = AnalogOutputFeedbackObject(
            objectIdentifier=('analogValue', i),
            objectName='analogValue-%d' % (i,),
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            relinquishDefault=0,
            priorityArray=priority_array,
        )
        bacnet.device.this_application.add_object(ravo)
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
