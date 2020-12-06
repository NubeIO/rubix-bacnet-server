from src.source_drivers.bacnet.services.network import Network


class Device:
    __instance = None

    @staticmethod
    def get_instance():
        if Device.__instance is None:
            Device()
        return Device.__instance

    def __init__(self):
        if Device.__instance is not None:
            raise Exception("Device class is a singleton!")
        else:
            Device.__instance = self

    def get_dev_url(self, device):
        return f"{device.bac_device_ip}:{device.bac_device_port}"

    def get_network(self, device):
        return Network.get_instance().get_network(device.network)

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
