import BAC0

from src.bacnet_master.interfaces.object_property import ObjProperty
from src.bacnet_server.helpers.helper_point_array import serialize_priority_array

bacnet = BAC0.lite(ip="192.168.15.102", mask=24, port=47808, ping=False)
h = 1
l = 203

print(bacnet.discover(networks=[1001],limits=(h, l)))

# print(bacnet.discover(networks=[1001]))
# print(bacnet.discover(networks='known'))
# print(bacnet.discover())
# print(bacnet.discover(networks='known', limits=(0,4194303), global_broadcast=False))
# print(bacnet.discover())
# print(bacnet.devices)

# print(bacnet.whois())
# print(bacnet.whois('10 1000'))
# print(bacnet.whois(global_broadcast=True))  # WhoIs broadcast globally.  Every device will respond with an IAm
# print(bacnet.whois('1001:31'))  # WhoIs looking for the device at (Network 1001, Address 31)
# print(bacnet.whois('1001:10 1000'))  # WhoIs looking for the device at (Network 1001, Devices in the ID range (10 - 1000))
# print(bacnet.whois('10 1000'))  # WhoIs looking for devices in the ID range (10 - 1000)
# print(bacnet.whois("1001:*"))  # all devices on network 1001
# print(bacnet.devices)

# read_vals = f' 192.168.15.202 device 202 objectList'
# #
# points = bacnet.read(read_vals)
# print(points)


def _common_whois(**kwargs):
    min_range = 0
    max_range = 4194302
    device_range_start = kwargs.get('range_start') or min_range
    if device_range_start < min_range:
        device_range_start = min_range
    device_range_end = kwargs.get('range_end') or max_range
    if device_range_end > max_range:
        device_range_end = max_range
    network_number = kwargs.get('network_number') or 0
    if network_number != 0:
        if 1 <= network_number <= 65534:
            return f'{network_number}:{device_range_start} {device_range_end}'
    else:
        return f'{device_range_start}:{device_range_end}'

print(_common_whois(network_number=1, range_start=1, range_end=3))
