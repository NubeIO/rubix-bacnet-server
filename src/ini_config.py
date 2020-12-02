"""Load configuration from .ini file."""
import configparser

import os

config = configparser.ConfigParser()
if os.environ.get("data_dir") is None:
    filename = 'settings/config.ini'
else:
    filename = os.path.join(os.environ.get("data_dir"), 'config.ini')

config.read(filename)

settings__enable_mqtt = config.getboolean('settings', 'enable_mqtt', fallback=False)
settings__enable_bacnet_server = config.getboolean('settings', 'enable_bacnet_server', fallback=True)

device__ip = config.get('device', 'ip', fallback='192.168.0.100')
device__port = config.getint('device', 'port', fallback=47808)
device__device_id = config.get('device', 'device_id', fallback='123')
device__local_obj_name = config.get('device', 'local_obj_name', fallback='Nube-IO')
device__model_name = config.get('device', 'model_name', fallback='rubix-bac-stack-RC4')
device__vendor_id = config.get('device', 'vendor_id', fallback='1173')
device__vendor_name = config.get('device', 'vendor_name', fallback='Nube iO Operations Pty Ltd')

mqtt__host = config.get('mqtt', 'host', fallback='0.0.0.0')
mqtt__port = config.getint('mqtt', 'port', fallback=1883)
mqtt__keepalive = config.getint('mqtt', 'keepalive', fallback=60)
mqtt__qos = config.getint('mqtt', 'qos', fallback=1)
mqtt__retain = config.getboolean('mqtt', 'retain', fallback=False)
mqtt__publish_value = config.getboolean('mqtt', 'publish_value', fallback=True)
mqtt__attempt_reconnect_on_unavailable = config.getboolean('mqtt', 'attempt_reconnect_on_unavailable', fallback=True)
mqtt__attempt_reconnect_secs = config.getint('mqtt', 'attempt_reconnect_secs', fallback=5)
mqtt__debug = config.getboolean('mqtt', 'debug', fallback=False)
