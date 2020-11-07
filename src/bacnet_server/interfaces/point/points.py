import enum


class BACnetPointType(enum.Enum):
    analogOutput = 0
    binaryOutput = 1




#     raw = 'raw'
#     int16 = 'int16',
#     uint16 = 'uint16',
#     int32 = 'int32',
#     uint32 = 'uint32',
#     float = 'float',
#     double = 'double',
#     digital = 'digital',




class ModbusPointUtils:
    mod_point_type = {
        "readCoils": "readCoils",
        "readDiscreteInputs": "readDiscreteInputs",
        "readHoldingRegisters": "readHoldingRegisters",
        "readInputRegisters": "readInputRegisters",
        "writeCoil": "writeCoil",
        "writeRegister": "writeRegister",
        "writeCoils": "writeCoils",
        "writeRegisters": "writeRegisters"
    }
    mod_point_data_type = {
        "raw": "raw",  # will be the array
        "int16": "int16",  # length of 1
        "uint16": "uint16",  # length of 1
        "int32": "int32",  # length of 2
        "uint32": "uint32",  # length of 2
        "float": "float",  # length of 2
        "double": "double",  # length of 4
        "digital": "digital",  # digital value true/false
    }
    mod_point_data_endian = {
        "LEB_BEW": "LEB_BEW",
        "LEB_LEW": "LEB_LEW",
        "BEB_LEW": "BEB_LEW",
        "BEB_BEW": "BEB_BEW"
    }


class ModbusPointUtilsFuncs:

    @classmethod
    def common_point_type(cls, _val: str) -> str:
        for key, value in ModbusPointUtils.mod_point_type.items():
            if _val == value:
                return _val
            raise Exception("point type is not correct")

    @classmethod
    def common_data_type(cls, _val: str) -> str:
        for key, value in ModbusPointUtils.mod_point_data_type.items():
            if _val == value:
                return _val
            raise Exception("data type is not correct")

    # @classmethod
    # def func_common_data_endian(cls, _val):
    #     for key, value in ModbusPointUtils.mod_point_data_endian.items():
    #         if _val == value:
    #             return _val
    #         raise Exception("endian is not correct")
