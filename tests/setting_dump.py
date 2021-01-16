from src import AppSetting, MqttSetting, BACnetSetting

if __name__ == '__main__':
    setting = '''
    {
      "bacnet": {
        "enabled": false,
        "ip": "192.168.0.100",
        "port": 47808,
        "device_id": 123,
        "local_obj_name": "Nube-IO",
        "model_name": "rubix-bac-stack-RC4",
        "vendor_id": 1173,
        "vendor_name": "Nube iO Operations Pty Ltd",
        "attempt_reconnect_secs": 5
      },
      "mqtt": {
        "enabled": false,
        "name": "bacnet-server-mqtt",
        "host": "0.0.0.0",
        "port": 1883,
        "keepalive": 60,
        "qos": 1,
        "retain": false,
        "attempt_reconnect_on_unavailable": true,
        "attempt_reconnect_secs": 5,
        "publish_value": true,
        "topic": "rubix/bacnet_server/points"
        "publish_debug": true,
        "debug_topic" = 'rubix/bacnet_server/debug'
      }
    }
    '''
    app_setting = AppSetting().reload(setting, is_json_str=True)
    print(type(app_setting.mqtt))
    print(type(app_setting.bacnet))
    print(type(app_setting.mqtt.enabled))
    assert app_setting.mqtt.enabled is False
    print('-' * 30)
    print(MqttSetting().serialize())
    print(BACnetSetting().serialize())
    print('-' * 30)
    print(AppSetting().serialize())
