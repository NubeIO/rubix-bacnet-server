import copy
import logging
import time
from random import randint
from typing import Union, Dict

from bacpypes.app import BIPSimpleApplication
from bacpypes.basetypes import EngineeringUnits, StatusFlags, DeviceStatus
from bacpypes.core import run as bacnet_run
from bacpypes.core import stop as bacnet_stop
from bacpypes.local.device import LocalDeviceObject
from bacpypes.local.object import Commandable, AnalogValueCmdObject, AnalogOutputCmdObject
from bacpypes.object import register_object_type, BinaryValueObject, BinaryOutputObject
from bacpypes.primitivedata import CharacterString
from bacpypes.service.object import ReadWritePropertyMultipleServices
from flask import current_app
from gevent import sleep

from src import BACnetSetting, AppSetting, FlaskThread, db
from src.bacnet_server.feedbacks.analog_output import AnalogOutputFeedbackObject, AnalogValueFeedbackObject, \
    BinaryOutputFeedbackObject, BinaryValueFeedbackObject
from src.bacnet_server.helpers.helper_point_array import default_values, create_object_identifier, \
    get_highest_priority_field, default_values_binary
from src.bacnet_server.helpers.helper_point_store import update_point_store
from src.bacnet_server.helpers.ip import IP
from src.bacnet_server.helpers.points import type_to_mqtt_topic
from src.bacnet_server.interfaces.point.points import PointType
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.models.model_server import BACnetServerModel
from src.mqtt import MqttClient
from src.utils import Singleton
from src.utils.project import get_version

logger = logging.getLogger(__name__)


class BACServer(metaclass=Singleton):

    def __init__(self):
        self.__config: Union[BACnetSetting, None] = None
        self.__bacnet_server: Union[BACnetServerModel, None] = None
        self.__registry: Dict[str, Commandable] = {}
        self.__sync_status: bool = False
        self.__running: bool = False
        self.ldo = None
        self.__bacnet = None
        self._thread = None

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
                    setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
                    if setting.mqtt.enabled:
                        mqtt_client = MqttClient()
                        while not mqtt_client.status():
                            logger.warning("MQTT is not connected, waiting for MQTT connection successful...")
                            time.sleep(self.config.attempt_reconnect_secs)
                        self.sync_stack()
                        self.__running = True
                    else:
                        self.sync_stack()
                        self.__running = True
                time.sleep(2)
            except Exception as e:
                logger.error(e)
                logger.warning("BACnet is not connected, waiting for BACnet server connection...")
                time.sleep(self.config.attempt_reconnect_secs)

    def stop_bacnet(self):
        if self.__bacnet:
            self.__bacnet.close_socket()
            bacnet_stop()

    def start_bacnet(self, bacnet_server):
        self.__bacnet_server = bacnet_server
        FlaskThread(target=self.connect, args=(bacnet_server,)).start()  # create_bacnet_stack

    def restart_bacnet(self, bacnet_server):
        if self.__bacnet:
            self.stop_bacnet()
        self.__reset_variable()
        self.start_bacnet(bacnet_server)

    def __reset_variable(self):
        self.ldo = None
        self.__bacnet = None
        self._thread = None
        self.__running = False
        self.__registry = {}

    def sync_stack(self):
        for point in BACnetPointModel.query.filter_by(object_type=PointType.analogOutput):
            self.add_point(point, False)
            sleep(0.001)
        for point in BACnetPointModel.query.filter_by(object_type=PointType.analogValue):
            self.add_point(point, False)
            sleep(0.001)
        for point in BACnetPointModel.query.filter_by(object_type=PointType.binaryValue):
            self.add_point(point, False)
            sleep(0.001)
        for point in BACnetPointModel.query.filter_by(object_type=PointType.binaryOutput):
            self.add_point(point, False)
            sleep(0.001)
        self.__sync_status = True
        self.__running = True

    def connect(self, bacnet_server: BACnetServerModel):
        address = self._ip_address(bacnet_server)
        version = get_version()
        description = "nube-io bacnet server"
        self.ldo = LocalDeviceObject(objectName=bacnet_server.local_obj_name,
                                     objectIdentifier=int(bacnet_server.device_id),
                                     maxApduLengthAccepted=1024,
                                     segmentationSupported="segmentedBoth",
                                     vendorIdentifier=bacnet_server.vendor_id,
                                     firmwareRevision=CharacterString(version),
                                     modelName=CharacterString(bacnet_server.model_name),
                                     vendorName=CharacterString(bacnet_server.vendor_name),
                                     description=CharacterString(description),
                                     systemStatus=DeviceStatus(1),
                                     applicationSoftwareVersion=CharacterString(version),
                                     databaseRevision=0)

        self.__bacnet = BIPSimpleApplication(self.ldo, address)
        self.__bacnet.add_capability(ReadWritePropertyMultipleServices)
        self.sync_stack()
        FlaskThread(target=bacnet_run).start()  # start bacpypes thread

    def add_point(self, point: BACnetPointModel, _update_point_store=True):
        [priority_array, present_value] = default_values_binary(point.priority_array_write, point.relinquish_default)
        if point.use_next_available_address:
            point.address = BACnetPointModel.get_next_available_address(point.address)
        object_identifier = create_object_identifier(point.object_type.name, point.address)
        if point.object_type.name == "analogOutput":
            register_object_type(AnalogOutputCmdObject)
            p = AnalogOutputFeedbackObject(
                profileName=point.uuid,
                objectIdentifier=(point.object_type.name, point.address),
                objectName=point.object_name,
                relinquishDefault=point.relinquish_default,
                presentValue=present_value,
                priorityArray=priority_array,
                eventState=point.event_state.name,
                statusFlags=StatusFlags(),
                units=EngineeringUnits(point.units.name),
                description=point.description,
                outOfService=False,
            )
            self.__bacnet.add_object(p)
            self.__registry[object_identifier] = p
        elif point.object_type.name == "analogValue":
            register_object_type(AnalogValueCmdObject)
            p = AnalogValueFeedbackObject(
                profileName=point.uuid,
                objectIdentifier=(point.object_type.name, point.address),
                objectName=point.object_name,
                relinquishDefault=point.relinquish_default,
                presentValue=present_value,
                priorityArray=priority_array,
                eventState=point.event_state.name,
                statusFlags=StatusFlags(),
                units=EngineeringUnits(point.units.name),
                description=point.description,
                outOfService=False,
            )
            self.__bacnet.add_object(p)
            self.__registry[object_identifier] = p
        elif point.object_type.name == "binaryOutput":
            pv = "inactive"
            rd = "inactive"
            if present_value > 0:
                pv = "active"
            if point.relinquish_default > 0:
                rd = "active"
            register_object_type(BinaryOutputObject)
            p = BinaryOutputFeedbackObject(
                profileName=point.uuid,
                objectIdentifier=(point.object_type.name, point.address),
                objectName=point.object_name,
                relinquishDefault=rd,
                presentValue=pv,
                priorityArray=priority_array,
                eventState=point.event_state.name,
                statusFlags=StatusFlags(),
                description=point.description,
                outOfService=False,
            )
            self.__bacnet.add_object(p)
            self.__registry[object_identifier] = p
        elif point.object_type.name == "binaryValue":
            pv = "inactive"
            rd = "inactive"
            if present_value > 0:
                pv = "active"
            if point.relinquish_default > 0:
                rd = "active"
            register_object_type(BinaryValueObject)
            p = BinaryValueFeedbackObject(
                profileName=point.uuid,
                objectIdentifier=(point.object_type.name, point.address),
                objectName=point.object_name,
                relinquishDefault=rd,
                presentValue=pv,
                priorityArray=priority_array,
                eventState=point.event_state.name,
                statusFlags=StatusFlags(),
                description=point.description,
                outOfService=False,
            )
            self.__bacnet.add_object(p)
            self.__registry[object_identifier] = p
        if _update_point_store:  # make it so on start of app not to update the point store
            update_point_store(point.uuid, present_value)
        else:
            db.session.commit()
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        if setting.mqtt.enabled:
            t = type_to_mqtt_topic(point.object_type.name)
            priority = get_highest_priority_field(point.priority_array_write)
            mqtt_client = MqttClient()
            mqtt_client.publish_value((t, object_identifier, point.object_name), present_value, priority)

    def remove_point(self, point):
        object_identifier = create_object_identifier(point.object_type.name, point.address)
        self.__bacnet.delete_object(self.__registry[object_identifier])
        del self.__registry[object_identifier]

    def remove_all_points(self):
        object_identifiers = copy.deepcopy(list(self.__registry.keys()))
        for object_identifier in object_identifiers:
            self.__bacnet.delete_object(self.__registry[object_identifier])
            del self.__registry[object_identifier]

    @classmethod
    def _ip_address(cls, bacnet_server: BACnetServerModel):
        if bacnet_server.enable_ip_by_nic_name:
            ip_by_nic_name = bacnet_server.ip_by_nic_name
            address = IP.get_nic_ipv4(ip_by_nic_name)
            return address
        else:
            ip = bacnet_server.ip
            port = bacnet_server.port
            mask = None
            try:
                ip, subnet_mask_and_port = ip.split("/")
                try:
                    mask, port = subnet_mask_and_port.split(":")
                except ValueError:
                    mask = subnet_mask_and_port
            except ValueError:
                ip = ip
            if not mask:
                mask = 24
            if not port:
                port = 47808
            address = "{}/{}:{}".format(ip, mask, port)
            return address
