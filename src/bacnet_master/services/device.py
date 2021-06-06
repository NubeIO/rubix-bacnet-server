import logging
import BAC0
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

    @staticmethod
    def build_url(device=None, **kwargs):
        if isinstance(device, dict):
            ip = kwargs.get('device_ip') or device.get("device_ip")
            mask = kwargs.get('device_mask') or device.get("device_mask")
            port = kwargs.get('device_port') or device.get("device_port")
        else:
            ip = kwargs.get('device_ip') or device.device_ip
            mask = kwargs.get('device_mask') or device.device_mask
            port = kwargs.get('device_port') or device.device_port
        if mask is not None:
            if port is not None:
                return f"{ip}/{mask}:{port}"
            else:
                return f"{ip}/{mask}"
        else:
            return ip

    def _common_point(self, point, device, **kwargs):
        dev_url = kwargs.get('dev_url') or self.build_url(device)
        network_number = kwargs.get('network_number') or device.network_number
        network_number = self._network_number(network_number)
        object_instance = kwargs.get('object_instance') or point.point_obj_id
        object_type = kwargs.get('object_type') or point.point_obj_type.name
        prop = kwargs.get('prop') or ObjProperty.presentValue.value
        type_mstp = kwargs.get('type_mstp') or device.type_mstp
        device_mac = kwargs.get('device_mac') or device.device_mac
        if type_mstp:
            return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        if network_number != 0:
            return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
        else:
            return f'{dev_url} {object_type} {object_instance} {prop}'

    def _common_object(self, device=None, **kwargs):
        """192.168.15.202/24:47808 device 202 objectList"""
        if isinstance(device, dict):
            dev_url = kwargs.get('dev_url') or self.build_url(device)
            type_mstp = kwargs.get('type_mstp') or device.get("type_mstp") or False
            device_mac = kwargs.get('device_mac') or device.get("type_mstp") or 0
            object_instance = kwargs.get('object_instance') or device.get("device_id")
            network_number = kwargs.get('network_number') or device.get("network_number")
            network_number = self._network_number(network_number)
        else:
            dev_url = kwargs.get('dev_url') or self.build_url(device)
            type_mstp = kwargs.get('type_mstp') or device.type_mstp or False
            device_mac = kwargs.get('device_mac') or device.device_mac
            object_instance = kwargs.get('object_instance') or device.device_id
            network_number = kwargs.get('network_number') or device.network_number
            network_number = self._network_number(network_number)
        object_type = kwargs.get('object_type') or ObjType.DEVICE.name
        prop = kwargs.get('prop') or ObjProperty.objectList.name
        print("type_mstp", type_mstp)
        if type_mstp == True:
            return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        if network_number != 0:
            return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
        else:
            return f'{dev_url} {object_type} {object_instance} {prop}'

    def _common_whois(self, **kwargs):
        device_range_start = kwargs.get('range_start')
        device_range_end = kwargs.get('range_end')
        network_number = kwargs.get('network_number')
        if network_number != 0:
            return f'{network_number}:{device_range_start} {device_range_end}'
        else:
            return f'{device_range_start} {device_range_end}'

    def _get_network_from_device(self, device):
        return Network.get_instance().get_network(device.network)

    def _get_network_from_network(self, network):
        return Network.get_instance().get_network(network)

    def _clean_point_value(self, payload):
        if isinstance(payload, (int, float)):
            return payload
        elif payload == "active":
            return 1
        elif payload == "inactive":
            return 0
        elif payload == True:
            return 1
        elif payload == False:
            return 0

    def _network_number(self, network_number):
        min_range = 0
        max_range = 65534
        if network_number == 0:
            return network_number
        elif network_number < min_range:
            return min_range
        elif network_number > max_range:
            return max_range
        else:
            return network_number

    def get_point_pv(self, point):
        device = BacnetDeviceModel.find_by_device_uuid(point.device_uuid)
        network_instance = self._get_network_from_device(device)
        read = self._common_point(point, device)
        try:
            if network_instance:
                return network_instance.read(read)
        except:
            return {}

    def read_point_list(self, device):
        network_instance = self._get_network_from_device(device)
        analog_inputs = []
        analog_outputs = []
        analog_values = []
        binary_input = []
        binary_output = []
        binary_value = []
        multi_state_input = []
        multi_state_output = []
        multi_state_value = []
        object_list = network_instance.read(self._common_object(device))
        obj_name = ObjProperty.objectName.name
        obj_present_value = ObjProperty.presentValue.name
        point_types = ["analogInput", "analogOutput", "analogValue", "binaryInput", "binaryOutput",
                       "binaryValue", "multiStateInput", "multiStateOutput", "multiStateValue"]
        for obj in object_list:
            object_type = obj[0]
            object_instance = obj[1]
            if object_type in point_types:
                try:
                    point_name = network_instance.read(
                        self._common_object(device,
                                            object_type=object_type,
                                            object_instance=object_instance,
                                            prop=obj_name))
                    point_value = network_instance.read(
                        self._common_object(device,
                                            object_type=object_type,
                                            object_instance=object_instance,
                                            prop=obj_present_value))
                    point = f"{obj[0]}_{obj[1]}"
                    point_value = self._clean_point_value(point_value)
                    if object_type == "analogInput":
                        analog_inputs.append({"point": point, "point_name": point_name, "point_value": point_value})
                    elif object_type == "analogOutput":
                        analog_outputs.append({"point": point, "point_name": point_name, "point_value": point_value})
                    elif object_type == "analogValue":
                        analog_outputs.append({"point": point, "point_name": point_name, "point_value": point_value})
                    elif object_type == "binaryInput":
                        binary_input.append({"point": point, "point_name": point_name, "point_value": point_value})
                    elif object_type == "binaryOutput":
                        binary_output.append({"point": point, "point_name": point_name, "point_value": point_value})
                    elif object_type == "binaryValue":
                        binary_value.append({"point": point, "point_name": point_name, "point_value": point_value})
                    elif object_type == "multiStateInput":
                        multi_state_input.append({"point": point, "point_name": point_name, "point_value": point_value})
                    elif object_type == "multiStateOutput":
                        multi_state_output.append(
                            {"point": point, "point_name": point_name, "point_value": point_value})
                    elif object_type == "multiStateValue":
                        multi_state_value.append({"point": point, "point_name": point_name, "point_value": point_value})
                except BAC0.core.io.IOExceptions.UnknownPropertyError:
                    continue

        points_list = {
            "analog_inputs": analog_inputs,
            "analog_outputs": analog_outputs,
            "analog_values": analog_values,
            "binary_input": binary_input,
            "binary_output": binary_output,
            "binary_value": binary_value,
            "multi_state_input": multi_state_input,
            "multi_state_output": multi_state_output,
            "multi_state_value": multi_state_value,
        }
        return points_list

    def get_object_list(self, device):
        network_instance = self._get_network_from_device(device)
        read = self._common_object(device)
        try:
            if network_instance:
                return network_instance.read(read)
        except:
            return {}

    def whois(self, net_uuid, **kwargs):
        net = BacnetNetworkModel.find_by_network_uuid(net_uuid)
        if not net:
            return {}
        network_instance = self._get_network_from_network(net)
        if not network_instance:
            return {}
        min_range = 0
        max_range = 4194302
        range_start = kwargs.get('range_start') or min_range
        if range_start < min_range:
            range_start = min_range
        range_end = kwargs.get('range_end') or max_range
        if range_end > max_range:
            range_end = max_range
        network_number = kwargs.get('network_number') or 0
        network_number = self._network_number(network_number)
        whois = kwargs.get('whois')
        global_broadcast = kwargs.get('global_broadcast')
        who = self._common_whois(range_start=range_start, range_end=range_end, network_number=network_number)
        logger.info(f"WHOIS network_id:{net_uuid} whois -> {whois} who {who}, global_broadcast:{global_broadcast} "
                    f", network_number:{network_number}")
        try:
            if whois:
                return network_instance.whois(who, global_broadcast)
            else:
                if network_number == 0:
                    logger.info(
                        f"WHOIS network_id:{net_uuid} discover -> range:{range_start},{range_end} , global_broadcast: {global_broadcast}")
                    network_instance.discover(limits=(range_start, range_end), global_broadcast=global_broadcast)
                    return network_instance.devices
                else:
                    logger.info(
                        f"WHOIS network_id:{net_uuid} discover -> network_number:{network_number} "
                        f"range:{range_start},{range_end}, global_broadcast:{global_broadcast}")
                    network_instance.discover(networks=[network_number], limits=(range_start, range_end),
                                              global_broadcast=global_broadcast)
                    return network_instance.devices
        except:
            return {}

    def unknown_get_object_list(self, net_uuid, device):
        net = BacnetNetworkModel.find_by_network_uuid(net_uuid)
        network_instance = self._get_network_from_network(net)
        read = self._common_object(device)
        logger.info(f"GET DEVICE OBJECT LIST  bac command {read}")
        try:
            if network_instance:
                return network_instance.read(read)
        except:
            return {}

    def write_point_present_value(self, device, obj, obj_instance, value, priority):
        dev_url = self.get_dev_url(device)
        network = self._get_network_from_device(device)
        if network:
            write = '%s %s %s presentValue %s - %s' % (dev_url, obj, obj_instance, value, priority)
            return network.write(write)
        raise Exception("Network not found")

    # def whois(self, network_uuid, whois, network_number):
    #     net = BacnetNetworkModel.find_by_network_uuid(network_uuid)
    #     if net is None:
    #         return {"error": "Network not found"}
    #     network = Network.get_instance().get_network(net)
    #     whois = to_bool(whois)
    #     if whois:
    #         network.whois()
    #     else:
    #         network.discover()
    #     if network:
    #         return network.devices
