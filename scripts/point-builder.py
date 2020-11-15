import json
import requests

ip = "192.168.0.100"
port = 1717

url = f'http://{ip}:{port}/api'
points_url = f'{url}/bacnet/points'

device_count = 50
device_start_address = 5
reg_address = [7, 8, 9, 11, 40]
point_names = ["Mode", "Fan_Status", "Setpoint", "Room_Temp", "Valve_position"]

is_looping = True
for i in range(device_count):
    i += device_start_address
    print("DEVICE:", i)
    for ii, r in enumerate(reg_address):
        addr = f'{i}{r}'
        addr = int(addr)
        # print(f'{i}{r}')
        name = point_names[ii]
        point_obj = {
            "object_type": "analogOutput",
            "object_name": f'dev_{i}_{name}',
            "address": addr,
            "relinquish_default": 1,
            "priority_array_write": {
                "_1": None,
                "_2": None,
                "_3": None,
                "_4": None,
                "_5": None,
                "_6": None,
                "_7": None,
                "_8": None,
                "_9": None,
                "_10": None,
                "_11": None,
                "_12": None,
                "_13": None,
                "_14": None,
                "_15": None,
                "_16": None
            },
            "event_state": "lowLimit",
            "units": "noUnits",
            "description": "description",
            "enable": True,
            "fault": False,
            "data_round": 0,
            "data_offset": 0

        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r_p = requests.post(f'{points_url}', data=json.dumps(point_obj), headers=headers)
        r_json = r_p.json()
        print(r_json)
        print(point_obj)
    if not is_looping:
        break
