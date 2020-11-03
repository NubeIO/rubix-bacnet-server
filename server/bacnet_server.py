import time
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from bacpypes.primitivedata import Real

from server.bacnet_device import device

executor = ThreadPoolExecutor(2)

app = Flask(__name__)
global bacnet

STATIC_BACNET_IP = '192.168.0.101/24'
STATIC_BACNET_PORT = "47808"
STATIC_BACNET_DEVICE_ID = 123
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
from tinydb import TinyDB, Query

db = TinyDB('points.json')
Points = Query()


def process_write(bac, point, val):
    change_value_real(bac, point, val)
    db.update({'present_value': val}, Points.name == point)
    res = process_read(bac, point)
    return res


def process_read(bac, point):
    obj = bac.this_application.get_object_name(point)
    print(1111)
    print(bac.this_application)
    value = obj.ReadProperty('presentValue')
    res = str(value)
    return res


def process_read_db(point):
    val = db.search(Points.name == point)
    res = str(val)
    return res


def change_value_real(bac, point, value):
    obj = bac.this_application.get_object_name(point)
    obj.presentValue = Real(value)



@app.route('/write/<val>')
def write(val=None):
    global bacnet
    val = float(val)
    res = executor.submit(process_write, bacnet, "ao_1", val)
    return res.result()


@app.route('/read')
def read():
    global bacnet
    value = executor.submit(process_read, bacnet, "ao_1")
    res = value.result(2)
    return res


def main():
    eth = STATIC_BACNET_IP
    ip = f"{eth}:{STATIC_BACNET_PORT}"
    device_id = STATIC_BACNET_DEVICE_ID
    print(ip)
    global bacnet

    bacnet = device(ip=ip, device_id=device_id)
    app.run(host=FLASK_HOST, port=FLASK_PORT, threaded=True)
    #
    while True:
        a = process_read(bacnet, "ao_1")
        val = float(a)
        db.update({'present_value': val}, Points.name == "ao_1")
        print(a)
        time.sleep(5)
        pass


if __name__ == "__main__":
    main()
