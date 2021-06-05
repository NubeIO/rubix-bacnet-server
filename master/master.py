import BAC0
import time
from flask import Flask, request, jsonify
import logging
import sys
import netifaces as ni

logging.basicConfig(filename='../log_bac0_app.log', level=logging.WARNING)

STATIC_BACNET_IP = '192.168.0.101/24'
STATIC_BACNET_PORT = "47808"
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
I_FACE = "enp0s31f6"


# fetches the subnet mask for the specified interface (ex. eth0, eth1) and converts to CIDR code
def get_subnet_mask(interface):
    netmask = ni.ifaddresses(interface)[ni.AF_INET][0]['netmask']
    return sum(bin(int(x)).count('1') for x in netmask.split('.'))


# Look for IP assigned to eth0 interface, assumes device is connected to BACnet network on eth0
logging.warning("Attempting to discover IP address on eth0 interface...")
try:
    i_face = I_FACE
    ni.ifaddresses(i_face)
    eth = ni.ifaddresses(i_face)[ni.AF_INET][0]['addr']
    eth = eth + '/' + str(get_subnet_mask(i_face))
    ip = f"{eth}:{STATIC_BACNET_PORT}"
    print(eth)
    bacnet = BAC0.connect(ip=ip)
    print("Discovered %s on for BACnet IP, connected" % ip)
except:
    logging.warning("Available interfaces: %s" % ni.interfaces())
    logging.warning(
        "Exception occured: %s \n Failed to read IP address on eth0, defaulting to static IP setting: %s" % (
            str(sys.exc_info()), STATIC_BACNET_IP))
    print("Establishing BACnet connection on: %s" % STATIC_BACNET_IP)
    bacnet = BAC0.connect(ip=STATIC_BACNET_IP)

time.sleep(1)
devices = bacnet.whois(global_broadcast=True)
device_mapping = {}
for device in devices:
    if isinstance(device, tuple):
        device_mapping[device[1]] = device[0]
        logging.warning("Detected device %s with address %s" % (str(device[1]), str(device[0])))
print(device_mapping)
print((str(len(device_mapping)) + " devices discovered on network."))

app = Flask(__name__)


# create endpoints
def create_server(app):
    @app.route('/read', methods=['POST'])
    def do_read():
        try:
            device_id = request.get_json().get('device_id')
            object_id = request.get_json().get('object_id')
            object_type = request.get_json().get('object_type')
            prop = request.get_json().get('prop')
        except:
            err_msg = "Read request was missing a required parameter. Required: [device_id, object_id, object_type]"
            logging.warning(err_msg + " Exception: " + str(sys.exc_info()))
            return jsonify({"status_code": 500, "description": err_msg})

        read = f"{device_id} {object_type} {object_id}  {prop}"
        try:
            result = bacnet.read(read)
            _type = ["0", "1", "active", "inactive"]
            rounded = None
            if result not in _type:
                try:
                    rounded = round(float(result), 1)
                except:
                    logging.warning("Failed to convert " + result + " to float for rounding.")
                result = rounded
        except:
            logging.warning("BACnet read failed. Exception: " + str(sys.exc_info()))
            return jsonify({"status_code": 500, "description": "BACnet read failed"})
        return jsonify({"status_code": 200, "value": result})

    @app.route('/write', methods=['POST'])
    def do_write():
        try:
            device_id = request.get_json().get('device_id')
            object_id = request.get_json().get('object_id')
            object_type = request.get_json().get('object_type')
            value = request.get_json().get('value')
        except:
            err_msg = "Write request was missing a required parameter. " \
                      "Required: [device_id, object_id, object_type, value]"
            logging.warning(err_msg)
            return jsonify({"status_code": 500, "description": err_msg})

        # create BACpypes write statement and run
        bp_stmt = '%s %s %s presentValue %s' % (device_id, object_type, object_id, value)
        logging.warning("Excecuting BACpypes statement: %s", bp_stmt)
        result = None
        try:
            result = bacnet.write(bp_stmt)
        except:
            logging.warning("BACnet write failed. Exception: " + str(sys.exc_info()))
            return jsonify({"status_code": 500, "description": "BACnet write failed"})
        return jsonify({"status_code": 200})

    return app


print("Creating server_old...")
app = create_server(app)

if __name__ == '__main__':
    print("Running BAC0 API server_old")
    app.run(host=FLASK_HOST, port=FLASK_PORT)
