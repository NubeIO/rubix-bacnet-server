import enum

from bacpypes.basetypes import EngineeringUnits

pointAO = {
    'object_identifier': 'object_identifier',  # int, unique
    'object_type': 'object_type',  # enum BACnetPointType,
    'object_name': 'object_name',  # str, unique
    'present_value': 'present_value',  # feedback from bacpypes
    'relinquish_default': 'relinquish_default',  # float CRUD from rest
    'priority_array': 'priority_array',  # feedback from bacpypes
    'priority_value': 'priority_value',  # float CRUD from rest
    'priority_num': 'priority_num',  # enum, CRUD from rest
    'units': 'units',  # enum, CRUD from rest
    'description': 'description',  # CRUD from rest

}


class BACnetPriorityNumber(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14
    FIFTEEN = 15
    SIXTEEN = 16
    NULL = 17


PriorityOperationEmergencyBool = ('Emergency On', 'Emergency Off', 'Auto')

PriorityOperationManualBool = ('Manual On', 'Manual Off', 'Auto')

PriorityOperationEmergencyNum = ('Emergency Value', 'Auto')

PriorityOperationManualNum = ('Manual Value', 'Auto')


class PriorityOperationBool(enum.Enum):
    ManualLifeSafety = PriorityOperationEmergencyBool
    AutomaticLifeSafety = 2
    Available_3 = 3
    Available_4 = 4
    Critical_Equipment_Control = 5
    Minimum_On_Off = 6
    Available_7 = 7
    Manual_Operator = PriorityOperationManualBool
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


print(PriorityOperationBool.get_list())


class PriorityOperationNum(enum.Enum):
    ManualLifeSafety = PriorityOperationEmergencyNum
    AutomaticLifeSafety = 2
    Available_3 = 3
    Available_4 = 4
    Critical_Equipment_Control = 5
    Minimum_On_Off = 6
    Available_7 = 7
    Manual_Operator = PriorityOperationManualNum
    Available_9 = 9
    Available_10 = 10
    Available_11 = 11
    Available_12 = 12
    Available_13 = 13
    Available_14 = 14
    Available_15 = 15
    Available_16 = 16



class PointType(enum.Enum):
    # analogInput= 0
    analogOutput = 1
    # analogValue= 2
    # binaryInput= 3
    binaryOutput = 2
    # binaryValue= 5


# get units from bacpypes lib
units = EngineeringUnits


class Units(enum.Enum):
    units_enum = units.enumerations


get_unit_enums = Units
# print(get_unit_enums.units_enum.value)
