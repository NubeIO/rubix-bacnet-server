from src.bacnet_master.interfaces.object_property import ObjProperty
from enum import Enum


class SupportedServices(Enum):
    acknowledgeAlarm = 'acknowledgeAlarm', 0
    confirmedCOVNotification = 'confirmedCOVNotification', 1
    confirmedEventNotification = 'confirmedEventNotification', 2
    getAlarmSummary = 'getAlarmSummary', 3
    getEnrollmentSummary = 'getEnrollmentSummary', 4
    subscribeCOV = 'subscribeCOV', 5
    atomicReadFile = 'atomicReadFile', 6
    atomicWriteFile = 'atomicWriteFile', 7
    addListElement = 'addListElement', 8
    removeListElement = 'removeListElement', 9
    createObject = 'createObject', 10
    deleteObject = 'deleteObject', 11
    readProperty = 'readProperty', 12
    # readPropertyConditional = 'readPropertyConditional',13      # removed in version 1 revision 12
    readPropertyMultiple = 'readPropertyMultiple', 14
    writeProperty = 'writeProperty', 15
    writePropertyMultiple = 'writePropertyMultiple', 16
    deviceCommunicationControl = 'deviceCommunicationControl', 17
    confirmedPrivateTransfer = 'confirmedPrivateTransfer', 18
    confirmedTextMessage = 'confirmedTextMessage', 19
    reinitializeDevice = 'reinitializeDevice', 20
    vtOpen = 'vtOpen', 21
    vtClose = 'vtClose', 22
    vtData = 'vtData', 23
    # = 'authenticate',24                 # removed in version 1 revision 11
    # = 'requestKey',25                   # removed in version 1 revision 11
    iAm = 'iAm', 26
    iHave = 'iHave', 27
    unconfirmedCOVNotification = 'unconfirmedCOVNotification', 28
    unconfirmedEventNotification = 'unconfirmedEventNotification', 29
    unconfirmedPrivateTransfer = 'unconfirmedPrivateTransfer', 30
    unconfirmedTextMessage = 'unconfirmedTextMessage', 31
    timeSynchronization = 'timeSynchronization', 32
    whoHas = 'whoHas', 33
    whoIs = 'whoIs', 34
    readRange = 'readRange', 35
    utcTimeSynchronization = 'utcTimeSynchronization', 36
    lifeSafetyOperation = 'lifeSafetyOperation', 37
    subscribeCOVProperty = 'subscribeCOVProperty', 38
    getEventInformation = 'getEventInformation', 39
    writeGroup = 'writeGroup', 40

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
        for i in SupportedServices:
            d[i.value[0]] = i.value[1]
        return d

    @classmethod
    def obj_as_false(self) -> dict:
        d = {}
        for i in SupportedServices:
            d[i.value[0]] = False
        return d

    @classmethod
    def obj_number(self) -> dict:
        d = {}
        for i in SupportedServices:
            d[i.value[1]] = [i.value[0], i.value[1]]
        return d

    @classmethod
    def check(self, ss):
        ss_dict = self.obj_as_false()
        ss_num = self.obj_number()
        for x in range(len(ss)):
            get_ss = ss_num.get(x)
            if get_ss is not None:
                if x == get_ss[1]:
                    if ss[x] == 1:
                        ss_dict[get_ss[0]] = True
        return ss_dict

