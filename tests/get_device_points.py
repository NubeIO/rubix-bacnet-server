import time

import BAC0

from src.bacnet_server.helpers.helper_point_array import serialize_priority_array

bacnet = BAC0.lite('192.168.15.102/24:47808')
# device = BAC0.device('192.168.15.202', 202, bacnet, segmentation_supported=True)
# points = device.points
# print(points)
#

# address = '192.168.15.189'
# object_type = 'device'
# object_instance = "10002:31"

# read_vals = f'{address} analogOutput 1 87'
#
# aa = bacnet.read(read_vals)
# for i in aa:
#     print(i)
# print(type(aa))

# read_vals = f' 102:31 device 1107 objectList'
# read_vals = f' 102:31 device 202 objectList'
#
# points = bacnet.read(read_vals)
# print(points)

# bacnet.read('10002:31 analogInput 1 presentValue')

# read_vals = f'{address} {object_type} {object_instance} 76'
# points = bacnet.read(read_vals)
# print(points)
# dicts = {}
# for pnt in points:
#     obj = pnt[0]
#     obj_id = pnt[1]
#     if not obj == "device":
#         read_present_value = f'{address} {obj} {obj_id} 85'
#         read_point_name = f'{address} {obj} {obj_id} 77'
#         # dicts[pnt] = points[points]
#         val = bacnet.read(read_present_value)
#         if val == "active":
#             val = 1
#         elif val == "inactive":
#             val = 0
#         time.sleep(0.2)
#         name = bacnet.read(read_point_name)
#         print(name, val)

# propertyListAnalog = ["objectName", "presentValue", "description", "deviceType", "statusFlags", "eventState",
#                       "reliability", "outOfService", "updateInterval", "units", "minPresValue", "maxPresValue",
#                       "resolution", "covIncrement", "timeDelay", "notificationClass", "highLimit", "lowLimit",
#                       "deadband", "limitEnable", "eventEnable"]


address = '192.168.15.202'
object_type = 'device'
object_instance = "202"
# object_instance = "10002:31"

propertyListAnalog = ["objectName", "presentValue", "units"]
objectPropertyList = {}
analogInputs = []
analogOutputs = []
analogValues = []
objectList = bacnet.read('%s device %s objectList' % (address, object_instance))
count = 0
for obj in objectList:
    objectType = obj[0]
    objectInstance = obj[1]
    count += 1
    if objectType == "analogInput":
        try:
            point_name = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, "objectName"))
            point_value = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, "presentValue"))
            point = f"{obj[0]}_{obj[1]}"
            analogInputs.append({"point": point, "point_name": point_name, "point_value": point_value})
        except BAC0.core.io.IOExceptions.UnknownPropertyError:
            continue
    elif objectType == "analogOutput":
        try:
            point_name = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, "objectName"))
            point_value = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, "presentValue"))
            point = f"{obj[0]}_{obj[1]}"
            analogOutputs.append({"point": point, "point_name": point_name, "point_value": point_value})
        except BAC0.core.io.IOExceptions.UnknownPropertyError:
            continue
    elif objectType == "analogValue":
        try:
            point_name = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, "objectName"))
            point_value = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, "presentValue"))
            point = f"{obj[0]}_{obj[1]}"
            analogValues.append({"point": point, "point_name": point_name, "point_value": point_value})
        except BAC0.core.io.IOExceptions.UnknownPropertyError:
            continue

objectPropertyList = {
    "analogInputs": analogInputs,
    "analogOutputs": analogOutputs,
    "analogValues": analogValues,
}

print(objectPropertyList)

# propertyListAnalog = ["objectName", "presentValue", "units"]
# objectPropertyList = {}
# analogInputs = {}
# analogOutputs = {}
# list = {}
# objectList = bacnet.read('%s device %s objectList' % (address, object_instance))
# for obj in objectList:
#     objectType = obj[0]
#     objectInstance = obj[1]
#     if objectType == "analogInput" or objectType == "analogOutput" or objectType == "analogValue":
#         for prop in propertyListAnalog:
#             point_name = None
#             point_value = None
#             try:
#                 if prop == "objectName":
#                     value = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, prop))
#                     e = f'{objectType}_{objectInstance}_name'
#                     if objectType == "analogInput":
#                         analogInputs[e] = value
#                     elif objectType == "analogOutput":
#                         analogOutputs[e] = value
#                     point_name = value
#                 elif prop == "presentValue":
#                     value = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, prop))
#                     e = f'{objectType}_{objectInstance}_value'
#                     if objectType == "analogInput":
#                         analogInputs[e] = value
#                     elif objectType == "analogOutput":
#                         analogOutputs[e] = value
#                     point_value = value
#                 elif prop == "units":
#                     value = bacnet.read('%s %s %s %s' % (address, objectType, objectInstance, prop))
#                     e = f'{objectType}_{objectInstance}_units'
#                     if objectType == "analogInput":
#                         analogInputs[e] = value
#                     elif objectType == "analogOutput":
#                         analogOutputs[e] = value
#             except BAC0.core.io.IOExceptions.UnknownPropertyError:
#                 continue
