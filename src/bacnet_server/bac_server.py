import time

import BAC0
from bacpypes.basetypes import EngineeringUnits

from src.bacnet_server.feedbacks.analog_output import AnalogOutputFeedbackObject
from src.bacnet_server.helpers.helper_mqtt import publish_mqtt_value
from src.bacnet_server.helpers.helper_point_array import default_values, create_object_identifier
from src.bacnet_server.helpers.helper_point_store import update_point_store
from src.bacnet_server.interfaces.point.points import PointType
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.models.model_server import BACnetServerModel


class BACServer:
    __instance = None

    def __init__(self):
        if BACServer.__instance:
            raise Exception("BACServer class is a singleton class!")
        else:
            self.__bacnet = None
            self.__registry = {}
            BACServer.__instance = self

    @staticmethod
    def get_instance():
        if BACServer.__instance is None:
            BACServer()
        return BACServer.__instance

    def is_running(self):
        return self.__bacnet is not None

    def start_bac(self):
        bacnet_server = BACnetServerModel.create_default_server_if_does_not_exist()
        self.connect(bacnet_server)
        self.sync_stack()

    def restart_bac(self, old_bacnet_server, new_bacnet_server, restart_on_failure=True):
        """
        It tries to establish connection with new configuration,
        If it fails it will re-establish connection with old one,
        Even this re-establishment with old one got error, we send an error message
        """

        if self.__bacnet:
            self.__bacnet.disconnect()  # on macOS it's not working
            time.sleep(1)  # as per their testing we need to sleep to make sure all sockets got closed
        self.__reset_variable()
        try:
            self.connect(new_bacnet_server)
            self.sync_stack()
        except Exception as e:
            print(f'Error: {str(e)}')
            if restart_on_failure:
                try:
                    BACServer.get_instance().restart_bac(old_bacnet_server, old_bacnet_server, False)
                except Exception as err:
                    print(f'Error on re-starting: {str(err)}')
                    raise Exception(f'Current configuration and even on revert server starting is got exception')
            raise e

    def sync_stack(self):
        for point in BACnetPointModel.query.filter_by(object_type=PointType.analogOutput):
            self.add_point(point)

    def connect(self, bacnet_server):
        self.__bacnet = BAC0.lite(ip=bacnet_server.ip,
                                  port=bacnet_server.port,
                                  deviceId=bacnet_server.device_id,
                                  localObjName=bacnet_server.local_obj_name,
                                  modelName=bacnet_server.model_name,
                                  vendorId=bacnet_server.vendor_id,
                                  vendorName=bacnet_server.vendor_name)

    def __reset_variable(self):
        self.__bacnet = None
        self.__registry = {}

    def add_point(self, point):
        [priority_array, present_value] = default_values(point.priority_array_write, 0.0)
        # TODO: Switch cases for different type of points
        object_identifier = create_object_identifier(point.object_type.name, point.address)
        ao = AnalogOutputFeedbackObject(
            profileName=point.uuid,
            objectIdentifier=(point.object_type.name, point.address),
            objectName=point.object_name,
            relinquishDefault=point.relinquish_default,
            presentValue=present_value,
            priorityArray=priority_array,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            units=EngineeringUnits(point.units.name),
            description=point.description,
        )
        self.__bacnet.this_application.add_object(ao)
        update_point_store(point.uuid, present_value)
        self.__registry[object_identifier] = ao
        publish_mqtt_value(object_identifier, present_value)

    def remove_point(self, point):
        object_identifier = create_object_identifier(point.object_type.name, point.address)
        self.__bacnet.this_application.delete_object(self.__registry[object_identifier])
        del self.__registry[object_identifier]
