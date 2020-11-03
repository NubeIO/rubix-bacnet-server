import BAC0
from bacpypes.local.object import (
    AnalogOutputCmdObject,
    AnalogValueCmdObject,
    BinaryOutputCmdObject,
    BinaryValueCmdObject,
)
from bacpypes.object import AnalogInputObject, register_object_type
from bacpypes.basetypes import EngineeringUnits
from bacpypes.primitivedata import CharacterString

import time


def device(ip, device_id):
    try:
        new_device = BAC0.lite(
            ip=ip, deviceId=device_id, localObjName="device test"
        )
    except Exception:
        new_device = BAC0.lite(deviceId=device_id, localObjName="device test")
    time.sleep(1)

    # Register class to activate behaviours
    register_object_type(AnalogOutputCmdObject, vendor_id=842)
    register_object_type(AnalogValueCmdObject, vendor_id=842)
    register_object_type(BinaryOutputCmdObject, vendor_id=842)
    register_object_type(BinaryValueCmdObject, vendor_id=842)

    bv_1 = BinaryValueCmdObject(
        objectIdentifier=("binaryValue", 1),
        objectName="bv_1",
        presentValue="inactive",
        description=CharacterString("Communication status on the serial interface"),
    )

    bo_1 = BinaryOutputCmdObject(
        objectIdentifier=("binaryOutput", 1),
        objectName="bo_1",
        presentValue="inactive",
        description=CharacterString("Turns the LED on or off"),
    )

    av_1 = AnalogValueCmdObject(
        objectIdentifier=("analogValue", 1),
        objectName="av_1",
        presentValue=0,
        units=EngineeringUnits("milliseconds"),
        description=CharacterString("Sets fade time between led colors (0-32767)"),
    )
    ai_1 = AnalogInputObject(
        objectIdentifier=("analogInput", 1),
        objectName="ai_1",
        presentValue=0,
        units=EngineeringUnits("percentRelativeHumidity"),
        description=CharacterString("Reading of humidity sensor"),
    )

    ao_1 = AnalogOutputCmdObject(
        objectIdentifier=("analogOutput", 1),
        objectName="ao_1",
        presentValue=0,
        description=CharacterString("Sets speed of heat exchanger"),
    )

    # BV
    new_device.this_application.add_object(bv_1)

    # BO
    new_device.this_application.add_object(bo_1)

    # AI
    new_device.this_application.add_object(ai_1)

    # AO
    new_device.this_application.add_object(ao_1)

    # AV
    new_device.this_application.add_object(av_1)

    return new_device
