from src.bacnet_master.interfaces.bacnet_calls import PointReadFunctions, DeviceReadFunctions
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
        return f"{device.device_ip}:{device.device_port}"

    def get_network(self, device):
        return Network.get_instance().get_network(device.network)

    def get_object_list(self, device):
        dev_url = self.get_dev_url(device)
        device_id = device.device_id
        network = self.get_network(device)
        if network:
            return network.read(f"{dev_url} device {device_id} objectList")
        raise Exception("Network not found")

    def get_points(self, device):
        dev_url = self.get_dev_url(device)
        device_id = device.device_id
        network = self.get_network(device)
        if network:
            return network.read(f"{dev_url} device {device_id} objectList")
        raise Exception("Network not found")

    # example point/76e9b1e6-4f3e-4391-9aba-93e1881ecfe4/analogInput/1/presentValue
    def get_point(self, device, obj, obj_instance, prop):
        device_ip = self.get_dev_url(device)
        network = self.get_network(device)
        if network:
            # bacnet.read('1:192.168.15.202/24:47808 analogInput 1 presentValue')
            # read = f"{dev_url} {obj} {obj_instance} {prop}"
            # device_ip, network_number, device_mac, device_id, type_mstp, obj, obj_instance
            read = PointReadFunctions.read_present_value(device_ip=device_ip)
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
        network = Network.get_instance().get_network(net)
        whois = to_bool(whois)
        if whois:
            network.whois()
        else:
            network.discover()
        if network:
            return network.devices
        raise Exception("Network not found")

    def get_unknown_device_objects(self, device_mac, device_id,
                                   device_ip,
                                   device_mask, device_port, network_uuid, type_mstp, network_number):
        net = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        network = Network.get_instance().get_network(net)
        req = DeviceReadFunctions.read_object_list(device_ip, device_id, device_mac=device_mac, type_mstp=type_mstp)
        print(11111)
        print(req)
        try:
            if network:
                return network.read(req)
        except:
            raise Exception("Network not found")
