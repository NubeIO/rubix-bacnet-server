import os
import time
import BAC0
from bacpypes.basetypes import PriorityArray, StatusFlags, PriorityValue, DateTime
from bacpypes.constructeddata import ArrayOf, Element, Choice, Any
from bacpypes.errors import ExecutionError
from bacpypes.local.object import AnalogValueCmdObject, BinaryOutputCmdObject
from bacpypes.object import Property, ReadableProperty
from bacpypes.object import register_object_type
from bacpypes.primitivedata import Atomic, BitString, Boolean, CharacterString, Date, Double, \
    Enumerated, Integer, Null, ObjectIdentifier, OctetString, Real, Time, \
    Unsigned, Unsigned16, Tag

from tinydb import TinyDB, Query

global bacnet
db = TinyDB('points.json')
Points = Query()


@register_object_type(vendor_id=999)
class BinaryOutputFeedbackObject(BinaryOutputCmdObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        priority_array = highest_priority(_priority_array)
        print(_priority_array)
        object_identifier = self.objectIdentifier
        object_name = self.objectName
        object_type = self.objectType
        present_value = self.presentValue
        #
        # priority_array = pnt_dict.get("priorityArray")
        # priority_array = highest_priority(priority_array)

        priority_pri_value = None
        # if priority_pri_value.Null is None:

        try:
            priority_pri_value = priority_array["value"]
            priority_pri_value = priority_pri_value.get('enumerated')
        except Exception:
            priority_pri_value = priority_pri_value

        priority_value = None
        try:
            priority_value = priority_array["priority"]
        except Exception:
            priority_value = priority_value

        print({"object_identifier": object_identifier,
               "object_name": object_name,
               "object_type": object_type,
               "_priority_array": _priority_array,
               "priority_value": priority_value,
               "priority_pri_value": priority_pri_value,
               "present_value": present_value})

        if new_value == self.presentValue:
            insert_if_none = db.search(Points.name == object_identifier)
            if not insert_if_none:  # first run
                db.insert({"object_identifier": object_identifier,
                           "object_name": object_name,
                           "object_type": object_type,
                           "_priority_array": _priority_array,
                           "priority_value": priority_value,
                           "priority_pri_value": priority_pri_value,
                           "present_value": present_value})
            elif insert_if_none:
                if priority_value == 1:
                    self.presentValue = "active"
                elif priority_value == 0:
                    self.presentValue = "inactive"
                db.update({"present_value": present_value,
                           "priority_value": priority_value,
                           "priority_pri_value": priority_pri_value},
                          Points.name == object_identifier)


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


class __PriorityArray(ArrayOf(
    PriorityValue, fixed_length=16, prototype=PriorityValue(null=()),
)):
    pass


class __PriorityValue(Choice):
    choiceElements = \
        [Element('null', Null)
            , Element('real', Real)
            , Element('enumerated', Enumerated)
            , Element('unsigned', Unsigned)
            , Element('boolean', Boolean)
            , Element('integer', Integer)
            , Element('double', Double)
            , Element('time', Time)
            , Element('characterString', CharacterString)
            , Element('octetString', OctetString)
            , Element('bitString', BitString)
            , Element('date', Date)
            , Element('objectidentifier', ObjectIdentifier)
            , Element('constructedValue', Any, 0)
            , Element('datetime', DateTime, 1)
         ]


def start():
    global bacnet
    bacnet = BAC0_Converter('192.168.0.101/24', 123, 'Pi')
    bacnet.start_device(47808)

    what_db_will_return = [{'null': ()}, {'null': ()}, {'null': ()}, {'null': ()}, {'null': ()}, {'null': ()},
                           {'null': ()},
                           {'null': ()}, {'null': ()}, {'null': ()}, {'null': ()}, {'null': ()}, {'null': ()},
                           {'null': ()},
                           {'null': ()}, {'enumerated': 1}]


    # call DB and build new array with existing results
    priority_array = PriorityArray()
    for i in range(16):
        PriorityValue(null=Null())

    # print(priority_array)
    # priority_array2 = PriorityArray()

    for i in range(1, RANDOM_OBJECT_COUNT + 1):
        ravo = BinaryOutputFeedbackObject(
            objectIdentifier=('binaryOutput', i),
            objectName='binaryOutput-%d' % (i,),
            presentValue="inactive",
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            feedbackValue="inactive",
            relinquishDefault="inactive",
            priorityArray=priority_array,
        )
        bacnet.device.this_application.add_object(ravo)

    for i in range(1, RANDOM_OBJECT_COUNT + 1):
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


if __name__ == '__main__':
    start()
