import enum

from bacpypes.basetypes import EngineeringUnits

PriorityOperationEmergencyBool = ('Emergency On', 'Emergency Off', 'Auto')

PriorityOperationManualBool = ('Manual On', 'Manual Off', 'Auto')

PriorityOperationEmergencyNum = ('Emergency Value', 'Auto')

PriorityOperationManualNum = ('Manual Value', 'Auto')


class PriorityOperationBool(enum.Enum):
    ManualLifeSafety = 1
    AutomaticLifeSafety = 2
    Available_3 = 3
    Available_4 = 4
    Critical_Equipment_Control = 5
    Minimum_On_Off = 6
    Available_7 = 7
    Manual_Operator = 8
    Available_9 = 9
    Available_10 = 10
    Available_11 = 11
    Available_12 = 12
    Available_13 = 13
    Available_14 = 14
    Available_15 = 15
    Available_16 = 16

    @staticmethod
    def get_list():
        return list(map(lambda c: c.value, PriorityOperationBool))


class PointType(enum.Enum):
    # analogInput= 0
    analogOutput = 1
    # analogValue= 2
    # binaryInput= 3
    # binaryOutput = 2
    # binaryValue= 5


class BACnetEventState(enum.Enum):
    normal = 0,
    fault = 1,
    offnormal = 2,
    highLimit = 3,
    lowLimit = 4,
    lifeSafetyAlarm = 5


class Units(enum.Enum):
    """
     get units from bacpypes lib
    """

    @staticmethod
    def return_units_dict():
        units = EngineeringUnits
        units_dict = units.enumerations
        return units_dict

    @staticmethod
    def return_units_enum():
        units = EngineeringUnits
        units_enum = units.enumerations
        _enum = enum.Enum('units', units_enum)
        return _enum


Units = Units.return_units_enum()
