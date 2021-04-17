import distutils

from src.bacnet_master.models.network import BacnetNetworkModel
from src.bacnet_master.services.network import Network
from src.bacnet_server.utils.functions import to_bool


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
        return f"{device.bac_device_ip}:{device.bac_device_port}"

    def get_network(self, device):
        return Network.get_instance().get_network(device.network)

    def get_object_list(self, device):
        dev_url = self.get_dev_url(device)
        bac_device_id = device.bac_device_id
        network = self.get_network(device)
        if network:
            return network.read(f"{dev_url} device {bac_device_id} objectList")
        raise Exception("Network not found")

    def get_points(self, device):
        dev_url = self.get_dev_url(device)
        bac_device_id = device.bac_device_id
        network = self.get_network(device)
        if network:
            return network.read(f"{dev_url} device {bac_device_id} objectList")
        raise Exception("Network not found")

    # example point/76e9b1e6-4f3e-4391-9aba-93e1881ecfe4/analogInput/1/presentValue
    def get_point(self, device, obj, obj_instance, prop):
        dev_url = self.get_dev_url(device)
        network = self.get_network(device)
        if network:
            read = f"{dev_url} {obj} {obj_instance} {prop}"
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
        print(net)
        network = Network.get_instance().get_network(net)
        print(6666666)
        print(network)
        print(net.network_ip)
        print(net.network_mask)
        print(net.network_port)

        whois = to_bool(whois)
        if whois:
            network.whois()
        else:
            network.discover()
        if network:
            return network.devices
        raise Exception("Network not found")

    def get_unknown_device_objects(self, bac_device_mac, bac_device_id,
                                   bac_device_ip,
                                   bac_device_mask, bac_device_port, network_uuid, type_mstp, network_number):
        print(333333333)
        net = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        print(net)
        print(333333333)
        network = Network.get_instance().get_network(net)
        # print(9999)
        # print(net.network_number)
        print(network)
        print(9999)
        # network_number = net.network_number
        type_mstp = to_bool(type_mstp)
        device_ip = f"{bac_device_ip}/{bac_device_mask}:{bac_device_port}"
        if type_mstp:
            req = f"{network_number}:{bac_device_mac} device {bac_device_id} objectList"
        else:
            req = f"{device_ip} device {bac_device_id} objectList"
        try:
            if network:
                return network.read(req)
        except:
            raise Exception("Network not found")

    def network_number(self, network_number: int) -> bool:
        if network_number == 0:
            return False
        else:
            return True
