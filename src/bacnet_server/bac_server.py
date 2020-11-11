import BAC0
from bacpypes.basetypes import EngineeringUnits
from bacpypes.primitivedata import CharacterString

from src.bacnet_server.config import NetworkConfig
from src.bacnet_server.feedbacks.analog_output import AnalogOutputFeedbackObject
from src.bacnet_server.helpers.helper_point_array import default_values, create_object_identifier
from src.bacnet_server.interfaces.point.points import PointType


class BACServer:
    __instance = None
    __bacnet = None

    def __init__(self):
        if BACServer.__instance:
            raise Exception("BACServer class is a singleton class!")
        else:
            ip = NetworkConfig.ip
            port = NetworkConfig.port
            device_id = NetworkConfig.deviceId
            local_obj_name = NetworkConfig.localObjName
            self.__bacnet = BAC0.lite(ip=ip, port=port, deviceId=device_id, localObjName=local_obj_name)
            BACServer.__instance = self

    @staticmethod
    def get_instance():
        if BACServer.__instance is None:
            BACServer()
        return BACServer.__instance

    def start_bac(self):
        from src.bacnet_server.models.model_point import BACnetPointModel

        for point in BACnetPointModel.query.filter_by(object_type=PointType.analogOutput):
            [priority_array, present_value] = default_values(point.priority_array_write, 0.0)
            ao = AnalogOutputFeedbackObject(
                objectIdentifier=(point.object_type.name, point.address),
                objectName=create_object_identifier(point.object_type.name, point.address),
                presentValue=present_value,
                priorityArray=priority_array,
                eventState="normal",
                statusFlags=[0, 0, 0, 0],
                relinquishDefault=0.0,
                units=EngineeringUnits("milliseconds"),
                description=CharacterString("Sets fade time between led colors (0-32767)"),
            )
            self.__bacnet.this_application.add_object(ao)
