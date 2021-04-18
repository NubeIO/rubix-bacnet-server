from enum import Enum


class ObjType(Enum):
    ANALOG_INPUT = "analog-input", 0, 'analogInput'
    ANALOG_OUTPUT = "analog-output", 1, 'analogOutput'
    ANALOG_VALUE = "analog-value", 2, 'analogValue'
    BINARY_INPUT = "binary-input", 3, 'binaryInput'
    BINARY_OUTPUT = "binary-output", 4, 'binaryOutput'
    BINARY_VALUE = "binary-value", 5, 'binaryValue'
    CALENDAR = "calendar", 6, 'calendar'
    COMMAND = "command", 7, 'command'
    DEVICE = "device", 8, 'device'
    EVENT_ENROLLMENT = "event-enrollment", 9, 'eventEnrollment'
    FILE = "file", 10, 'file'
    GROUP = "group", 11, 'group'
    LOOP = "loop", 12, 'loop'
    MULTI_STATE_INPUT = "multi-state-input", 13, 'multiStateInput'
    MULTI_STATE_OUTPUT = "multi-state-output", 14, 'multiStateOutput'
    NOTIFICATION_CLASS = "notification-class", 15, 'notificationClass'
    PROGRAM = "program", 16, 'program'
    SCHEDULE = "schedule", 17, 'schedule'
    AVERAGING = "averaging", 18, 'averaging'
    MULTI_STATE_VALUE = "multi-state-value", 19, 'multiStateValue'
    TREND_LOG = "trend-log", 20, 'trendLog'
    LIFE_SAFETY_POINT = "life-safety-point", 21, 'lifeSafetyPoint'
    LIFE_SAFETY_ZONE = "life-safety-zone", 22, 'lifeSafetyZone'
    ACCUMULATOR = "accumulator", 23, 'accumulator'
    PULSE_CONVERTER = "pulse-converter", 24, 'pulseConverter'
    ACCESS_POINT = "access-point", 33, 'accessPoint'

    @property
    def id(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[2]

    @property
    def name_dashed(self):
        return self.value[0]

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def all_obj(self) -> dict:
        d = {}
        for i in ObjType:
            d[i.value[2]] = i.value[1]
        return d

    @classmethod
    def obj_as_false(self) -> dict:
        d = {}
        for i in ObjType:
            d[i.value[2]] = False
        return d

