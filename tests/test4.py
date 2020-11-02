import os
import time
import BAC0
from bacpypes.basetypes import PriorityArray
from bacpypes.errors import ExecutionError
from bacpypes.local.object import AnalogValueCmdObject
from bacpypes.object import Property, ReadableProperty
from bacpypes.object import register_object_type
from bacpypes.primitivedata import Real
from tinydb import TinyDB, Query
from itertools import count

global bacnet
db = TinyDB('points.json')
Points = Query()

global cnt
COUNT = 0


# def count():
#     global cnt
#     cnt += 1
#     return cnt
def increment():
    global COUNT
    COUNT = COUNT + 1


priority_array = {
    'in1': None,
    'in2': None,
    'in3': None,
    'in4': None,
    'in5': None,
    'in6': None,
    'in7': None,
    'in8': None,
    'in9': None,
    'in10': None,
    'in11': None,
    'in12': None,
    'in13': None,
    'in14': None,
    'in15': None,
    'in16': None,
}


class PointProperty(Property):

    def __init__(self, identifier):
        print("__init__ %r", identifier)
        Property.__init__(self, identifier, Real, default=0.0, optional=True, mutable=False)

    def ReadProperty(self, obj, arrayIndex=None):
        print("------------------------------------ReadProperty-----------------------------------------------")
        print(obj, arrayIndex)
        # access an array
        if arrayIndex is not None:
            raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')
        a = obj.__dict__
        x = a.get("_values")
        point = x.get("objectName")
        val = db.search(Points.name == point)
        # print(val.index("present_value"))
        print(type(val))
        value = None
        for d in val:
            if 'present_value' in d:
                value = d['present_value']

        return value

    def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
        # print(obj, value, arrayIndex, priority, direct)

        # insert_if_none = db.search(Points.name.exists())

        # if (priority is not None) and not (1 <= priority <= 16):
        #     raise ValueError("invalid priority (1..16)")
        # print("---WriteProperty---", obj, value, arrayIndex, priority, direct)
        a = obj.__dict__
        x = a.get("_values")
        point = x.get("objectName")
        pri = x.get("priorityArray")
        print("---WriteProperty---", point, value, arrayIndex, pri, direct)
        insert_if_none = db.search(Points.name == point)
        increment()
        print(COUNT)
        # and count < 1

        if not insert_if_none:  # first run
            db.insert({'name': point, 'present_value': 0, "priority_array": priority_array})
        elif insert_if_none and COUNT > 1:
            db.update({'present_value': value }, Points.name == point)


class AvObject(AnalogValueCmdObject):
    properties = [
        PointProperty('presentValue'),
        ReadableProperty('priorityArray', PriorityArray),
        # PointProperty('priorityArray'),
    ]

    def __init__(self, **kwargs):
        AnalogValueCmdObject.__init__(self, **kwargs)


register_object_type(AvObject)
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
        ravo = AvObject(
            objectIdentifier=('analogValue', i),
            objectName='Random-%d' % (i,),
            statusFlags=[0, 0, 0, 0],
            # priorityArray=PriorityArray(),
        )
        # print("    - ravo: %r", ravo)
        bacnet.device.this_application.add_object(ravo)
    global cnt
    while True:
        time.sleep(0.2)


if __name__ == '__main__':
    start()
