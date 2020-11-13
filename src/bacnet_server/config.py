import configparser
import os
import pwd

user = pwd.getpwuid(os.getuid()).pw_dir

file = f"{user}/bacnet_server.ini"
config = configparser.ConfigParser()


class NetworkConfig:
    ip = None
    deviceId = None
    localObjName = None
    port = None

    def __init__(self, ip, deviceId, localObjName, port):
        self.ip = ip
        self.deviceId = deviceId
        self.localObjName = localObjName
        self.port = port


# TODO remove
class PointConfig:
    bo_count = None
    ao_count = None

    def __init__(self, ao_count, bo_count):
        self.ao_count = ao_count
        self.bo_count = bo_count


class DbConfig:
    location = None
    name = None

    def __init__(self, location, name):
        self.location = location
        self.name = name


try:
    f = open(file, 'r')
    config.read_file(f)
    # get device
    NetworkConfig.ip = config.get("device", "ip")
    NetworkConfig.deviceId = config.get("device", "deviceId")
    NetworkConfig.localObjName = config.get("device", "localObjName")
    NetworkConfig.port = config.get("device", "port")
    # get point config
    PointConfig.ao_count = config.get("points", "ao_count")
    PointConfig.bo_count = config.get("points", "bo_count")
    # json db location OLD #TODO remove
    # DbConfig.location = config.get("db", "location")
    # DbConfig.name = config.get("db", "name")


except OSError as e:
    print('File cannot be opened: ', e)
