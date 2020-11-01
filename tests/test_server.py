import logging
import time

import BAC0
from BAC0.core.devices.create_objects import create_AV, create_AO
from BAC0.tasks.RecurringTask import RecurringTask
from bacpypes.basetypes import EngineeringUnits
from bacpypes.primitivedata import Real, CharacterString, Enumerated

logging.basicConfig(filename='log_bac0_app.log', level=logging.INFO)


def changeValueOfMyAI():
    obj = bacnet.this_application.get_object_name('MyAI')
    value = obj.ReadProperty('presentValue').value
    value = value + 1 if value < 100 else 0
    obj.presentValue = Real(value)


ip = '192.168.0.101/24:47809'
deviceId = 111
localObjName = "BAC0_Fireplace"

bacnet = BAC0.lite(ip=ip, deviceId=deviceId, localObjName=localObjName)
bacnet.this_application.add_object(create_AO(oid=1, name='MyAI', pv=Real(0), pv_writable=True))
# task = RecurringTask(changeValueOfMyAI, delay=5)
# task.start()

# av = []
# current_humidity = create_AO(
#     oid=1, name="MyAI", pv=1, pv_writable=False
# )
# current_humidity.description = CharacterString(
#     "Current Humidity in percent relative humidity"
# )
# av.append(current_humidity)
#
# current_temp = create_AV(oid=1, name="Current_Temp", pv=0, pv_writable=False)
# current_temp.units = EngineeringUnits("degreesFahrenheit")
# current_temp.description = CharacterString("Current Temperature in degF")
# av.append(current_temp)
#
# for each in av:
#     bacnet.this_application.add_object(each)


def myprint(d):
    for k, v in d.items():
        if isinstance(v, dict):
            myprint(v)
        else:
            print("{0} : {1}".format(k, v))


# def read_priority_array(self):
#     """
#         Retrieve priority array of the point
#         """
#     if self.properties.priority_array != False:
#         try:
#             res = self.properties.device.properties.network.read(
#                 "{} {} {} priorityArray".format(
#                     self.properties.device.properties.address,
#                     self.properties.type,
#                     str(self.properties.address),
#                 ),
#                 vendor_id=self.properties.device.properties.vendor_id,
#             )
#             self.properties.priority_array = res
#         except ValueError:
#             self.properties.priority_array = False
#         except Exception as e:
#             raise Exception(
#                 "Problem reading : {} | {}".format(self.properties.name, e)
#             )


# def priority(self, priority=None):
#     if not self.properties.priority_array:
#         return None
#
#     self.read_priority_array()
#     if not priority:
#         return self.properties.priority_array.debug_contents()
#     if priority < 1 or priority > 16:
#         raise IndexError("Please provide priority to read (1-16)")
#
#     else:
#         pa = self.properties.priority_array.value[priority]
#         try:
#             key, value = zip(*pa.dict_contents().items())
#             if key[0] == "null":
#                 return None
#             else:
#                 return key[0], value[0]
#         except ValueError:
#             return None






while True:
    # obj = bacnet.this_application.iter_objects('MyAI')
    obj = bacnet.this_application.get_object_name("MyAI")  # BAC0_Fireplace
    attrs = vars(obj)
    print(obj.__dict__)
    # print(dir(obj))

    # print(bacnet.this_application)
    # print(obj.presentValue)
    # print(obj.priorityArray)
    # # obj1 = bacnet.this_application
    # attrs = vars(obj)
    # print(attrs.items())
    #

    # priority_array = obj.priorityArray
    # for i in range(1, 17):
    #     priority_value = priority_array[i]
    #     print(priority_value)
    #     if priority_value.null is None:
    #       print("    - found at index: %r", i)
        # if issubclass(Real, Enumerated):
        #     print(234234)
        #     value = Real._xlate_table[value]
    # pa = a.value[1]
    # print(pa)
    # print(type(pa))
    # attrs = vars(pa)
    # print(attrs)
    #
    # value = pa.cast_out()
    # pa = self.properties.priority_array.value[priority]
    # pa = attrs[1]
    # print(type(pa))
    # try:
    #     key, value = zip(*pa.dict_contents().items())
    #     print(2222222, key, value)
    #     if key[0] == "null":
    #         print("111 none")
    #     else:
    #         print(key[0], value[0])
    # except ValueError:
    #     print("2222 none")
    # # values = attrs['_values']
    # # print(values)
    # # # print(obj.keys())
    # # # attrs = vars(obj)
    # # # # print(attrs.keys())
    # values = attrs['_values']
    # print(values.items())
    # # p = values['priorityArray']
    # print(type(obj))
    # print(p.PriorityValue())
    # print(obj.priorityArray.__dict__.items())
    # attr = vars(obj.priorityArray)
    # print(type(attr))
    # values = attr['value']
    # one = values[1]
    # print(one.__dict__.items())

    # print(type(values))
    # print(obj.priorityArray.keys())
    # print(p.keys())
    # print(attrs['_values'])
    # print(attrs.values())
    # print("values")
    # print(attrs.items())
    # print("items")
    # a = obj.priorityArray
    # pa = a.value[1]
    # aa = myprint(attrs)
    # print(aa)
    # key, value = zip(*a.dict_contents().items())

    # print(type(a))
    # print(a)
    # for key in a:
    #     print(key, '->', a[key])
    # print(type(attrs))
    # print(attrs.values())
    # # print(obj.priorityArray.__dict__.keys())
    #
    # print(obj)
    # print(', '.join("%s: %s" % item for item in attrs.items()))
    # print("type(bacnet)")
    # print(type(bacnet.this_application))
    # print(bacnet.this_application.get_services_supported())
    # print(bacnet.this_application)

    # print("type(type(bacnet.this_application))")
    # print('Running and value is {}'.format(obj.presentValue))
    time.sleep(5)
# ws_list = []
# WeeklySchedule = ArrayOf(DailySchedule) # Type
#
# for schedule in weekly_schedule:
# tv_list = []
# for event in schedule:
# tv = TimeValue(time=(10,0,0,0), value=Real(10.0))
# tv_list.append(tv)
# ws_list.append(DailySchedule(daySchedule=tv_list))
# ws_object = WeeklySchedule(ws_list)
#
# value = Any()
# value.cast_in(ws_object)
# request = WritePropertyRequest(objectIdentifier=("schedule", 302), propertyIdentifier="weeklySchedule")
# request.pduDestination = Address('XX:XX:XX:XX')
# request.propertyValue = value
# request.propertyArrayIndex = 1
# request.priority = 16
#
# iocb = IOCB(request)
# iocb.set_timeout(10)
# deferred(device.this_application.request_io, iocb)
#
# iocb.wait()
