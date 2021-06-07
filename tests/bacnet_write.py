import time

import BAC0

bacnet = BAC0.lite()

# Write null @ 16
# address = '192.168.15.202'
# object_type = 'analogOutput'
# object_instance = "1"
# value = 22.2  # write Null
# bacnet.write('address object object_instance property value - priority')
# 1001:46 analogOutput 1 85 1 - 16
bacnet.write(f'1001:46 analogOutput 2 presentValue 1 - 16')

# read_vals = f'{address} {object_type} {object_instance} 85 '
# time.sleep(1)
# print(bacnet.read(read_vals))
#
#
# # Write 11 @ 1
# address = '192.168.15.10'
# object_type = 'analogOutput'
# object_instance = "1"
# value = 11.1  # write Null
# bacnet.write(f'{address} {object_type} {object_instance} presentValue {value} - 1')
#
# read_vals = f'{address} {object_type} {object_instance} 85'
# time.sleep(1)
# print(bacnet.read(read_vals))
#
# # Write null @ 1
# address = '192.168.15.202'
# object_type = 'analogOutput'
# object_instance = "1"
# value = 'null'  # write Null
# bacnet.write(f'{address} {object_type} {object_instance} presentValue {value} - 1')
#
# read_vals = f'{address} {object_type} {object_instance} 85'
# time.sleep(1)
# print(bacnet.read(read_vals))


