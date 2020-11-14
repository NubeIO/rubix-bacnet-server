import requests

ip = "0.0.0.0"
port = 1717

url = f'http://{ip}:{port}/api'

points_url = f'{url}/bacnet/points'
reg_address = [1, 2, 3, 4, 5, 6, 7]
reg_names = ["point", "point", "point", "point", "point", "point", "point"]

print(points_url)

for i, r in enumerate(reg_address):
    name = reg_names[i]
    point_obj = {
        "object_type": "analogOutput",
        "object_name": f'{name}/{r}',
        "address": r,
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
        "units": "noUnits",
        "description": "description",
        "enable": True,
        "fault": False,
        "data_round": 0,
        "data_offset": 0

    }
    r_p = requests.post(f'{points_url}', json=point_obj)
    r_json = r_p.json()
    print(r_json)
    print(point_obj)
