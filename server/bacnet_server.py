from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from bacpypes.primitivedata import Real

# from server.bacnet_device import device
from server.bacnet_device import *

executor = ThreadPoolExecutor(2)

app = Flask(__name__)
global bacnet

STATIC_BACNET_IP = '192.168.0.101/24'
STATIC_BACNET_PORT = "47808"
STATIC_BACNET_DEVICE_ID = 111
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001


@app.route('/jobs/<val>')
def run_jobs(val=None):
    executor.submit(some_long_task1)
    global bacnet
    val = float(val)
    res = executor.submit(some_long_task2, bacnet, "ao_1", val)
    print(22222)
    print(22222)
    return res.result()


@app.route('/aa')
def run():
    return 'Taa'


def some_long_task1():
    print("Task #1 started!")
    print("Task #1 is done!")


def some_long_task2(bac, point, val):
    change_value(bac, point, val)
    read = get_value(bac, point)
    rtn = str(read)
    return rtn


def get_value(bac, point):
    obj = bac.this_application.get_object_name(point)
    value = obj.ReadProperty('presentValue').value
    return value


def change_value(bac, point, value):
    obj = bac.this_application.get_object_name(point)
    obj.presentValue = Real(value)


def main():
    eth = STATIC_BACNET_IP
    ip = f"{eth}:{STATIC_BACNET_PORT}"
    device_id = STATIC_BACNET_DEVICE_ID
    print(ip)
    global bacnet
    bacnet = device(ip=ip, device_id=device_id)
    app.run(host=FLASK_HOST, port=FLASK_PORT, threaded=False)

    while True:
        pass


@app.route('/')
def hello_world():
    # a = get_value(bacnet, point)
    # print(a)
    return 'Hello, World!'


if __name__ == "__main__":
    main()
