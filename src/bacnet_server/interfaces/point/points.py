import enum

from bacpypes.basetypes import EngineeringUnits

priority_array = {
    '_1': None,
    '_2': None,
    '_3': None,
    '_4': None,
    '_5': None,
    '_6': None,
    '_7': None,
    '_8': None,
    '_9': None,
    '_10': None,
    '_11': None,
    '_12': None,
    '_13': None,
    '_14': None,
    '_15': None,
    '_16': None,
}


class PriorityNumber(enum.Enum):
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    _11 = 11
    _12 = 12
    _13 = 13
    _14 = 14
    _15 = 15
    _16 = 16
    NULL = 17


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
    binaryOutput = 2
    # binaryValue= 5


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