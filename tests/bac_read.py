import time

from bacpypes.basetypes import ServicesSupported

import BAC0

from src.bacnet_master.interfaces.device_supported_services import SupportedServices

bacnet = BAC0.lite()
#
# # Write null @ 16
# address = '192.168.15.196'
# object_type = 'device'
# object_instance = "1234"
#
# read_vals = f'{address} {object_type} {object_instance} 97'

# aaa = SupportedServices.get(address, object_type, object_instance)
# print(aaa)
# #
# ss = bacnet.read(read_vals)
# print(ss)
# print(SupportedServices.check(ss))
# # print(aaaa)

# <addr> <type> <inst> <prop>
print(bacnet.read('192.168.15.202/24:47808 analogOutput 1 presentValue'))  # or 85
print(bacnet.read('192.168.15.202/24:47808 analogOutput 1 85'))
# print(bacnet.read('202 analogOutput 1 85'))
print(bacnet.read('192.168.15.202/24:47808 device 202 objectList'))  # or 76
print(bacnet.read('192.168.15.202/24:47808 device 202 76'))
# for x in range(len(ss)):
#     print(22222)
#     print(x)
# # def get_key(val):
#     for key, value in types.items():
#         if val == value:
#             return key
#
#     return "key doesn't exist"
#
#
# readProperty = get_key(14)
# print(aa)

number = 1

if 1 <= number <= 65534:
    print(1111)
