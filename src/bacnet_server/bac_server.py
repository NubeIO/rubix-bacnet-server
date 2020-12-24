import copy
from logging import Logger

import BAC0
import time
from bacpypes.basetypes import EngineeringUnits

from src import BACnetSetting
from src.bacnet_server.feedbacks.analog_output import AnalogOutputFeedbackObject
from src.bacnet_server.helpers.helper_point_array import default_values, create_object_identifier
from src.bacnet_server.helpers.helper_point_store import update_point_store
from src.bacnet_server.interfaces.point.points import PointType
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.models.model_server import BACnetServerModel
from src.bacnet_server.mqtt_client import MqttClient
from src.utils import Singleton


class BACServer(metaclass=Singleton):

    def __init__(self):
        self.logger = None
        self.__config = None
        self.__bacnet = None
        self.__registry = {}
        self.__sync_status = False

    @property
    def config(self) -> BACnetSetting:
        return self.__config

    def status(self):
        return self.config and self.config.enabled and self.__bacnet and self.__sync_status

    def start_bac(self, config: BACnetSetting, logger: Logger):
        self.logger = logger or Logger(__name__)
        self.__config = config
        bacnet_server = BACnetServerModel.create_default_server_if_does_not_exist(self.config)
        self.keep_connecting(bacnet_server)
        mqttc = MqttClient()
        if mqttc.config.enabled and mqttc.config.publish_value:
            while not mqttc.status():
                logger.warning("MQTT is not connected, waiting for MQTT connection successful...")
                time.sleep(mqttc.config.attempt_reconnect_secs)
        self.sync_stack()

    def keep_connecting(self, bacnet_server):
        try:
            self.connect(bacnet_server)
        except Exception as e:
            self.logger.error(e)
            self.logger.warning("BACnet is not connected, waiting for BACnet server connection...")
            time.sleep(self.config.attempt_reconnect_secs)
            self.keep_connecting(bacnet_server)

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
            self.logger.error(e)
            if restart_on_failure:
                try:
                    self.restart_bac(old_bacnet_server, old_bacnet_server, False)
                except Exception as err:
                    self.logger.error(f'Error on re-starting: {str(err)}')
                    raise Exception(f'Current configuration and even on revert server starting is got exception')
            raise e

    def sync_stack(self):
        for point in BACnetPointModel.query.filter_by(object_type=PointType.analogOutput):
            self.add_point(point)
        self.__sync_status = True

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
            eventState=point.event_state.name,
            statusFlags=[0, 0, 0, 0],
            units=EngineeringUnits(point.units.name),
            description=point.description,
        )
        self.__bacnet.this_application.add_object(ao)
        update_point_store(point.uuid, present_value)
        self.__registry[object_identifier] = ao
        mqttc = MqttClient()
        if mqttc.config.publish_value:
            mqttc.publish_mqtt_value(object_identifier, present_value)

    def remove_point(self, point):
        object_identifier = create_object_identifier(point.object_type.name, point.address)
        self.__bacnet.this_application.delete_object(self.__registry[object_identifier])
        del self.__registry[object_identifier]

    def remove_all_points(self):
        object_identifiers = copy.deepcopy(list(self.__registry.keys()))
        for object_identifier in object_identifiers:
            self.__bacnet.this_application.delete_object(self.__registry[object_identifier])
            del self.__registry[object_identifier]
