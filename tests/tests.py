from enum import Enum

from src.bacnet_master.interfaces.device_supported_services import SupportedServices

aa = [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

class SupportedServices2(Enum):
    subscribeCOV = "subscribeCOV", 5
    readProperty = "readProperty", 12
    whoHas = "whoHas", 33

    @property
    def id(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def all_obj(self) -> dict:
        d = {}
        for i in SupportedServices2:
            d[i.value[0]] = i.value[1]
        return d

    @classmethod
    def obj_as_false(self) -> dict:
        d = {}
        for i in SupportedServices2:
            d[i.value[0]] = False
        return d

print(SupportedServices2.obj_as_false())

# def check(self, ss):
#     supported_services = SupportedServices.supported_services
#     ss_dict = supported_services
#     for x, y in supported_services.items():
#         ss_dict[x] = False
#     for x in range(len(ss)):
#         if x == supported_services.get("subscribeCOV"):
#             ss_dict['subscribeCOV'] = True
#         if x == supported_services.get("whoHas"):
#             ss_dict['whoHas'] = True
#         if x == supported_services.get("whoIs"):
#             ss_dict['whoIs'] = True
#         if x == supported_services.get("iAm"):
#             ss_dict['iAm'] = True
#         if x == supported_services.get("iHave"):
#             ss_dict['iHave'] = True
#         if x == supported_services.get("subscribeCov"):
#             ss_dict['subscribeCov'] = True
#         if x == supported_services.get("readProperty"):
#             ss_dict['readProperty'] = True
#         if x == supported_services.get("readPropertyMultiple"):
#             ss_dict['readPropertyMultiple'] = True
#         if x == supported_services.get("writeProperty"):
#             ss_dict['writeProperty'] = True
#         if x == supported_services.get("writePropertyMultiple"):
#             ss_dict['writePropertyMultiple'] = True
#         if x == supported_services.get("readRange"):
#             ss_dict['readRange'] = True
#         if x == supported_services.get("timeSynchronization"):
#             ss_dict['timeSynchronization'] = True
#         if x == supported_services.get("utcTimeSynchronization"):
#             ss_dict['utcTimeSynchronization'] = True
#         return ss_dict
