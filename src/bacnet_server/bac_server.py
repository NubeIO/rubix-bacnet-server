import copy
import logging
import time
from typing import Union, Dict

import BAC0
from bacpypes.basetypes import EngineeringUnits
from bacpypes.local.object import Commandable

from src import BACnetSetting
from src.bacnet_server.feedbacks.analog_output import AnalogOutputFeedbackObject
from src.bacnet_server.helpers.helper_point_array import default_values, create_object_identifier
from src.bacnet_server.helpers.helper_point_store import update_point_store
from src.bacnet_server.interfaces.point.points import PointType
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.models.model_server import BACnetServerModel
from src.mqtt import MqttClient
from src.utils import Singleton

logger = logging.getLogger(__name__)


class BACServer(metaclass=Singleton):

    def __init__(self):
        self.__config: Union[BACnetSetting, None] = None
        self.__bacnet: Union[BAC0, None] = None
        self.__bacnet_server: Union[BACnetServerModel, None] = None
        self.__registry: Dict[str, Commandable] = {}
        self.__sync_status: bool = False
        self.__running: bool = False

    @property
    def config(self) -> Union[BACnetSetting, None]:
        return self.__config

    def status(self) -> bool:
        return bool(self.config and self.config.enabled and self.__bacnet and self.__sync_status)

    def start_bac(self, config: BACnetSetting):
        self.__config = config
        self.__bacnet_server = BACnetServerModel.create_default_server_if_does_not_exist(self.config)
        self.loop_forever()

    def loop_forever(self):
        while True:
            try:
                if not self.__running:
                    self.connect(self.__bacnet_server)
                    mqtt_client = MqttClient()
                    if mqtt_client.config.enabled and mqtt_client.config.publish_value:
                        while not mqtt_client.status():
                            logger.warning("MQTT is not connected, waiting for MQTT connection successful...")
                            time.sleep(self.config.attempt_reconnect_secs)
                    self.sync_stack()
                    self.__running = True
                time.sleep(2)
            except Exception as e:
                logger.error(e)
                logger.warning("BACnet is not connected, waiting for BACnet server connection...")
                time.sleep(self.config.attempt_reconnect_secs)

    def restart_bac(self, bacnet_server):
        if self.__bacnet:
            self.__bacnet.disconnect()  # on macOS it's not working
            time.sleep(1)  # as per their testing we need to sleep to make sure all sockets got closed

        self.__reset_variable()
        self.__bacnet_server = bacnet_server

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
        self.__running = False
        self.__registry = {}

    def add_point(self, point):
        [priority_array, present_value] = default_values(point.priority_array_write, 0.0)
        # TODO: Switch cases for different type of points
        if point.use_next_available_address:
            point.address = BACnetPointModel.get_next_available_address(point.address)
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
        mqtt_client = MqttClient()
        mqtt_client.publish_value(('ao', object_identifier), present_value)

    def remove_point(self, point):
        object_identifier = create_object_identifier(point.object_type.name, point.address)
        self.__bacnet.this_application.delete_object(self.__registry[object_identifier])
        del self.__registry[object_identifier]

    def remove_all_points(self):
        object_identifiers = copy.deepcopy(list(self.__registry.keys()))
        for object_identifier in object_identifiers:
            self.__bacnet.this_application.delete_object(self.__registry[object_identifier])
            del self.__registry[object_identifier]
