import logging

import BAC0

from src.bacnet_master.interfaces.bacnet_calls import PointReadFunctions, DeviceReadFunctions, BACnetCommon
from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.interfaces.object_property import ObjProperty
from src.bacnet_master.models.device import BacnetDeviceModel
from src.bacnet_master.models.network import BacnetNetworkModel
from src.bacnet_master.services.network import Network
from src.bacnet_server.utils.functions import to_bool

logger = logging.getLogger(__name__)


class Device:
    __instance = None

    @staticmethod
    def get_instance():
        if Device.__instance is None:
            Device()
        return Device.__instance

    def __init__(self):
        if Device.__instance is not None:
            print("Device class is a singleton! @ Binod to check")
            # raise Exception("Device class is a singleton!")
        else:
            Device.__instance = self

    def get_dev_url(self, device):
        return f"{device.device_ip}:{device.device_port}"

    def build_url(self, device):
        ip = device.device_ip
        mask = device.device_mask
        port = device.device_port
        if mask is not None:
            if port is not None:
                return f"{ip}/{mask}:{port}"
            else:
                return f"{ip}/{mask}"
        else:
            return ip

    def _common_point(self, point, device, **kwargs):
        dev_url = self.build_url(device)
        network_number = device.network_number
        object_instance = point.point_obj_id
        object_type = kwargs.get('object_type') or point.point_obj_type.name
        prop = kwargs.get('prop') or ObjProperty.presentValue.value
        type_mstp = device.type_mstp
        device_mac = device.device_mac
        if network_number != 0:
            if 1 <= network_number <= 65534:
                return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
            if type_mstp:
                return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        else:
            return f'{dev_url} {object_type} {object_instance} {prop}'

    def _common_object(self, device, **kwargs):
        """192.168.15.202/24:47808 device 202 objectList"""
        dev_url = self.build_url(device)
        network_number = device.network_number
        object_instance = kwargs.get('object_instance') or device.device_id
        object_type = kwargs.get('object_type') or ObjType.DEVICE.name
        prop = kwargs.get('prop') or ObjProperty.objectList.name
        type_mstp = device.type_mstp
        device_mac = device.device_mac
        print(f'{dev_url} {object_type} {object_instance} {prop}')
        if network_number != 0:
            if 1 <= network_number <= 65534:
                return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
            if type_mstp:
                return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        else:
            return f'{dev_url} {object_type} {object_instance} {prop}'

    def get_network(self, device):
        return Network.get_instance().get_network(device.network)

    def get_point2(self, point):
        device = BacnetDeviceModel.find_by_device_uuid(point.device_uuid)
        network_instance = self.get_network(device)
        read = self._common_point(point, device)
        try:
            if network_instance:
                return network_instance.read(read)
        except:
            return {}

    def read_point_list(self, device):
        network_instance = self.get_network(device)
        analog_inputs = []
        analog_outputs = []
        analog_values = []
        object_list = network_instance.read(self._common_object(device))
        obj_name = ObjProperty.objectName.name
        obj_present_value = ObjProperty.presentValue.name
        for obj in object_list:
            object_type = obj[0]
            object_instance = obj[1]
            if object_type == "analogInput":
                try:
                    point_name = network_instance.read(
                        self._common_object(device, object_type=object_type, object_instance=object_instance, prop=obj_name))
                    point_value = network_instance.read(
                        self._common_object(device, object_type=object_type, object_instance=object_instance, prop=obj_present_value))
                    point = f"{obj[0]}_{obj[1]}"
                    analog_inputs.append({"point": point, "point_name": point_name, "point_value": point_value})
                except BAC0.core.io.IOExceptions.UnknownPropertyError:
                    continue
            elif object_type == "analogOutput":
                try:
                    point_name = network_instance.read(
                        self._common_object(device, object_type=object_type, object_instance=object_instance, prop=obj_name))
                    point_value = network_instance.read(
                        self._common_object(device, object_type=object_type, object_instance=object_instance, prop=obj_present_value))
                    point = f"{obj[0]}_{obj[1]}"
                    analog_outputs.append({"point": point, "point_name": point_name, "point_value": point_value})
                except BAC0.core.io.IOExceptions.UnknownPropertyError:
                    continue
            elif object_type == "analogValue":
                try:
                    point_name = network_instance.read(
                        self._common_object(device, object_type=object_type, object_instance=object_instance, prop=obj_name))
                    point_value = network_instance.read(
                        self._common_object(device, object_type=object_type, object_instance=object_instance, prop=obj_present_value))
                    point = f"{obj[0]}_{obj[1]}"
                    analog_values.append({"point": point, "point_name": point_name, "point_value": point_value})
                except BAC0.core.io.IOExceptions.UnknownPropertyError:
                    continue
        points_list = {
            "analog_inputs": analog_inputs,
            "analog_outputs": analog_outputs,
            "analog_values": analog_values,
        }
        return points_list

    def get_object_list(self, device):
        # device = BacnetDeviceModel.find_by_device_uuid(point.device_uuid)
        network_instance = self.get_network(device)
        read = self._common_point(point, device)
        try:
            if network_instance:
                return network_instance.read(read)
        except:
            return {}

        # dev_url = self.build_url(device)
        # device_id = device.device_id
        # network = self.get_network(device)
        # if network:
        #     return network.read(f"{dev_url} device {device_id} objectList")
        # raise Exception("Network not found")

    def get_points(self, device):
        dev_url = self.get_dev_url(device)
        device_id = device.device_id
        network = self.get_network(device)
        if network:
            return network.read(f"{dev_url} device {device_id} objectList")
        raise Exception("Network not found")

    # example point/76e9b1e6-4f3e-4391-9aba-93e1881ecfe4/analogInput/1/presentValue
    def get_point(self, device, obj, obj_instance, prop):
        dev_url = self.build_url(device)
        network = self.get_network(device)

        if network:
            # bacnet.read('1:192.168.15.202/24:47808 analogInput 1 presentValue')
            read = f"{dev_url} {obj} {obj_instance} {prop}"
            # device_ip, network_number, device_mac, device_id, type_mstp, obj, obj_instance
            # read = PointReadFunctions.read_present_value(device_ip=dev_url)
            return network.read(read)
        raise Exception("Network not found")

    def write_point_present_value(self, device, obj, obj_instance, value, priority):
        dev_url = self.get_dev_url(device)
        network = self.get_network(device)
        if network:
            write = '%s %s %s presentValue %s - %s' % (dev_url, obj, obj_instance, value, priority)
            return network.write(write)
        raise Exception("Network not found")

    def whois(self, network_uuid, whois, network_number):
        net = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if net is None:
            return {"error": "Network not found"}
        network = Network.get_instance().get_network(net)
        whois = to_bool(whois)
        if whois:
            network.whois()
        else:
            network.discover()
        if network:
            return network.devices

    # def get_object(self, network_uuid, device_ip,  device_id,  **kwargs):
    #     # dev_url = self.build_url(device)
    #     # device_id = device.device_id
    #     # network = self.get_network(device)
    #     net = BacnetNetworkModel.find_by_network_uuid(network_uuid)
    #     if net is None:
    #         return {"error": "Network not found"}
    #     network = Network.get_instance().get_network(net)
    #     if network is None:
    #         return {"error": "Network not found"}
    #     req = DeviceReadFunctions.read_object_list(device_ip, device_id)
    #     try:
    #         if network:
    #             return network.read(req)
    #     except:
    #         return {}

    def get_object(self, network_uuid, device_ip, device_id, **kwargs):
        # dev_url = self.build_url(device)
        # device_id = device.device_id
        # network = self.get_network(device)
        net = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if net is None:
            return {"error": "Network not found"}
        network = Network.get_instance().get_network(net)
        if network is None:
            return {"error": "Network not found"}
        req = DeviceReadFunctions.read_object_list(device_ip, device_id)
        try:
            if network:
                return network.read(req)
        except:
            return {}
