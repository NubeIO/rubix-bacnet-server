import BAC0
from bacpypes.basetypes import EngineeringUnits
from bacpypes.primitivedata import CharacterString

from src.bacnet_server.config import NetworkConfig
from src.bacnet_server.feedbacks.analog_output import AnalogOutputFeedbackObject
from src.bacnet_server.helpers.helper_point_array import default_values, create_object_identifier
from src.bacnet_server.helpers.helper_point_store import update_point_store
from src.bacnet_server.interfaces.point.points import PointType


class BACServer:
    __instance = None

    def __init__(self):
        if BACServer.__instance:
            raise Exception("BACServer class is a singleton class!")
        else:
            ip = NetworkConfig.ip
            port = NetworkConfig.port
            device_id = NetworkConfig.deviceId
            local_obj_name = NetworkConfig.localObjName
            self.__bacnet = BAC0.lite(ip=ip, port=port, deviceId=device_id, localObjName=local_obj_name)
            self.__registry = {}
            BACServer.__instance = self

    @staticmethod
    def get_instance():
        if BACServer.__instance is None:
            BACServer()
        return BACServer.__instance

    def start_bac(self):
        from src.bacnet_server.models.model_point import BACnetPointModel

        for point in BACnetPointModel.query.filter_by(object_type=PointType.analogOutput):
            self.add_point(point)

    def add_point(self, point):
        [priority_array, present_value] = default_values(point.priority_array_write, 0.0)
        # TODO: Switch cases for different type of points
        object_identifier = create_object_identifier(point.object_type.name, point.address)
        ao = AnalogOutputFeedbackObject(
            objectIdentifier=(point.object_type.name, point.address),
            objectName=point.uuid,
            presentValue=present_value,
            priorityArray=priority_array,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            relinquishDefault=0.0,
            units=EngineeringUnits("milliseconds"),
            description=CharacterString("Sets fade time between led colors (0-32767)"),
        )
        update_point_store(point.uuid, present_value)
        self.__registry[object_identifier] = ao
        self.__bacnet.this_application.add_object(ao)

    def remove_point(self, point):
        object_identifier = create_object_identifier(point.object_type.name, point.address)
        self.__bacnet.this_application.delete_object(self.__registry[object_identifier])
