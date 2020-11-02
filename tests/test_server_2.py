import os
import random

import BAC0
from BAC0.core.utils.notes import note_and_log
from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.errors import ExecutionError
from bacpypes.object import AnalogValueObject, Property, register_object_type
from bacpypes.local.object import (AnalogValueCmdObject, BinaryValueCmdObject)
from bacpypes.object import register_object_type, AnalogValueObject
from bacpypes.basetypes import EngineeringUnits
from bacpypes.primitivedata import CharacterString
from bacpypes.primitivedata import Real
import time

objects = []


class BAC0_Converter():
    analog_value_num = 400
    analog_value_list = []
    binary_value_num = 0
    binary_value_list = []

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

    def build_analog(self, input_device, input_dev_point):
        global objects
        self.input_device = input_device
        self.input_dev_point = input_dev_point
        register_object_type(AnalogValueCmdObject, vendor_id=842)
        av_object = AnalogValueCmdObject(
            objectIdentifier=("analogValue", BAC0_Converter.analog_value_num),
            objectName=self.input_dev_point,
            presentValue=666,
            description=CharacterString(f"imported from {self.input_device}: {self.input_dev_point} "))
        BAC0_Converter.analog_value_num += 1
        BAC0_Converter.analog_value_list.append(av_object)
        self.device.this_application.add_object(av_object)
        return av_object

    def update_analogs(self, name, value):
        global objects
        av = self.device.this_application.get_object_name(name)
        if av:
            av.presentValue = value
            print(f"AV present Value: {av.presentValue}")

    def build_binary(self, input_device, input_dev_point):
        self.input_device = input_device
        self.input_dev_point = input_dev_point
        register_object_type(BinaryValueCmdObject, vendor_id=842)
        bv_object = BinaryValueCmdObject(
            objectIdentifier=("binaryValue", BAC0_Converter.binary_value_num),
            objectName=self.input_dev_point,
            presentValue='inactive',
            description=CharacterString(f"imported from {self.input_device}: {self.input_dev_point} "))
        BAC0_Converter.binary_value_num += 1
        BAC0_Converter.binary_value_list.append(bv_object)
        self.device.this_application.add_object(bv_object)
        return bv_object


_debug = 0
_log = ModuleLogger(globals())


class RandomValueProperty(Property):

    def __init__(self, identifier):
        if _debug: RandomValueProperty._debug("__init__ %r", identifier)
        Property.__init__(self, identifier, Real, default=0.0, optional=True, mutable=False)

    def ReadProperty(self,
                     obj, arrayIndex=None):
        print(obj, arrayIndex)
        if _debug: RandomValueProperty._debug("ReadProperty %r arrayIndex=%r", obj, arrayIndex)

        # access an array
        if arrayIndex is not None:
            raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')

        # return a random value
        value = random.random() * 100.0
        # if _debug: RandomValueProperty._debug("    - value: %r", value)

        return value

    def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
        print(obj, value, arrayIndex, priority, direct)
        if _debug: RandomValueProperty._debug("WriteProperty %r %r arrayIndex=%r priority=%r direct=%r", obj, value,
                                              arrayIndex, priority, direct)


#
#   Random Value Object Type
#

class RandomAnalogValueObject(AnalogValueObject):
    properties = [
        RandomValueProperty('presentValue'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomAnalogValueObject._debug("__init__ %r", kwargs)
        AnalogValueObject.__init__(self, **kwargs)


bacpypes_debugging(RandomAnalogValueObject)
register_object_type(RandomAnalogValueObject)
RANDOM_OBJECT_COUNT = int(os.getenv('RANDOM_OBJECT_COUNT', 10))


def start():
    Toast = BAC0_Converter('192.168.0.101/24', 123, 'Pi')
    Toast.start_device(47808)
    Toast.build_analog('modbus_dev_1', 'register_1')
    Toast.build_analog('modbus_dev_1', 'register_2')
    Toast.build_binary('modbus_dev_1', 'register_3')
    Toast.build_binary('modbus_dev_1', 'register_4')

    # make some random input objects
    for i in range(1, RANDOM_OBJECT_COUNT + 1):
        ravo = RandomAnalogValueObject(
            objectIdentifier=('analogValue', i),
            objectName='Random-%d' % (i,),
        )
        print("    - ravo: %r", ravo)
        Toast.device.this_application.add_object(ravo)

    for i in Toast.analog_value_list:
        print(i)
    for i in Toast.binary_value_list:
        print(i)
    while True:
        # print(Toast.device.this_device)
        # for i in Toast.binary_value_list:
        #     print(i)
        time.sleep(2)


if __name__ == '__main__':
    start()
