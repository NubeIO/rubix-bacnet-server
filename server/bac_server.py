import BAC0
from bacpypes.basetypes import EngineeringUnits
from bacpypes.local.object import AnalogOutputCmdObject, BinaryOutputCmdObject
from bacpypes.primitivedata import CharacterString, Real, Enumerated
from flask_restful import reqparse

from server.breakdowns.helper_point_array import default_values, create_object_identifier
from server.breakdowns.point_save_on_change import point_save
from tinydb import TinyDB, Query
from server.config import PointConfig, NetworkConfig, DbConfig
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify
import paho.mqtt.client as mqtt

executor = ThreadPoolExecutor(2)
app = Flask(__name__)

global bacnet
db_location = DbConfig.location
db_name = DbConfig.name
db_file = f"{db_location}/{db_name}.json"
db = TinyDB(db_file)
Points = Query()

client = mqtt.Client()
client.connect("0.0.0.0", 1883, 60)


class BinaryOutputFeedbackObject(BinaryOutputCmdObject):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._property_monitors["presentValue"].append(self.check_feedback)

    def check_feedback(self, old_value, new_value):
        pnt_dict = self._dict_contents()
        object_identifier = create_object_identifier(self.objectIdentifier)
        object_name = self.objectName
        object_type = self.objectType
        present_value = self.presentValue
        _type = "enumerated"
        point_save(pnt_dict, object_identifier, object_name, object_type,
                   present_value, _type, old_value, new_value, db, Points)


class AnalogOutputFeedbackObject(AnalogOutputCmdObject):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._property_monitors["presentValue"].append(self.check_feedback)

    def check_feedback(self, old_value, new_value):
        pnt_dict = self._dict_contents()
        object_identifier = create_object_identifier(self.objectIdentifier)
        object_name = self.objectName
        object_type = self.objectType
        present_value = self.presentValue
        if isinstance(present_value, Real):
            present_value = present_value.value
        elif type(present_value) is float:
            present_value = present_value
        _type = "real"
        topic = f"bacnet/server/points/ao/{object_identifier}"
        payload = str(present_value)
        client.publish(topic, payload, qos=1, retain=True)
        point_save(pnt_dict, object_identifier, object_name, object_type,
                   present_value, _type, old_value, new_value, db, Points)


def start():
    global bacnet
    ao_count = PointConfig.ao_count
    bo_count = PointConfig.bo_count

    ip = NetworkConfig.ip
    port = NetworkConfig.port
    device_id = NetworkConfig.deviceId
    local_obj_name = NetworkConfig.localObjName
    bacnet = BAC0.lite(ip=ip, port=port, deviceId=device_id, localObjName=local_obj_name)

    for i in range(1, int(bo_count) + 1):
        default_pv = 'inactive'
        object_type = 'binaryOutput'
        [priority_array, present_value] = default_values(object_type, i, default_pv, db, Points)
        bo = BinaryOutputFeedbackObject(
            objectIdentifier=(object_type, i),
            objectName='binaryOutput-%d' % (i,),
            presentValue=present_value,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            feedbackValue="inactive",
            relinquishDefault="inactive",
            priorityArray=priority_array,
            description=CharacterString("Sets fade time between led colors (0-32767)"),
        )
        bacnet.this_application.add_object(bo)
    for i in range(1, int(ao_count) + 1):
        default_pv = 0.0
        object_type = 'analogOutput'
        [priority_array, present_value] = default_values(object_type, i, default_pv, db, Points)
        ao = AnalogOutputFeedbackObject(
            objectIdentifier=(object_type, i),
            objectName='analogOutput-%d' % (i,),
            presentValue=present_value,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            relinquishDefault=0.0,
            priorityArray=priority_array,
            units=EngineeringUnits("milliseconds"),
            description=CharacterString("Sets fade time between led colors (0-32767)"),
        )
        bacnet.this_application.add_object(ao)

    app.run(host='0.0.0.0', port=5001, threaded=True)
    while True:
        pass


def process_write(bac, point, val):
    change_value_real(bac, point, val)
    db.update({'presentValue': val}, Points.object_identifier == point)  # update DB
    res = process_read(bac, point)
    return res


def process_read(bac, point):
    """this will read the BACnet AO value"""
    obj = bac.this_application.get_object_name(point)
    value = obj.ReadProperty('presentValue')
    res = value
    return res


def process_read_db(point):
    val = db.search(Points.object_identifier == point)
    res = str(val)
    return res


def change_value_real(bac, point, value):
    """this will write the BACnet for an AO value"""
    obj = bac.this_application.get_object_name(point)
    value = float(value)
    obj.presentValue = Real(value)


def change_value_bool(bac, point, value):
    obj = bac.this_application.get_object_name(point)
    value = int(value)
    obj.presentValue = Enumerated(value)


def change_point_name(bac, point, value):
    obj = bac.this_application.get_object_name(point)
    value = int(value)
    obj.presentValue = Enumerated(value)


@app.route('/points/write/ao', methods=['POST'])
def write():
    global bacnet
    parser = reqparse.RequestParser()
    parser.add_argument('point', type=str, help='bacnet point object id`', required=True)
    parser.add_argument('value', type=float, help='value must be a float', required=True)
    parser.add_argument('priority', type=int, help='priority must be a number', required=False)
    args = parser.parse_args()
    point = args['point']
    value = args['value']
    priority = args['priority']
    res = executor.submit(process_write, bacnet, point, float(value))
    res = res.result()
    res = vars(res).get('value')
    return jsonify(res)


@app.route('/points/read/<point>', methods=['GET'])
def read(point=None):
    global bacnet
    value = executor.submit(process_read, bacnet, point)
    res = value.result(2)
    return res


@app.route('/points/ao', methods=['GET'])
def read_all():
    get = db.search(Points.object_type == 'analogOutput')
    print(get)
    all_ids = []
    for dct in get:
        all_ids.append({'name': f'{dct["object_name"]} -> {dct["object_name"]}', 'object_identifier':
            dct["object_identifier"], 'object_name': dct["object_name"], 'object_type': dct["object_type"],
                        'highest_priority_array': dct["highest_priority_array"]})
    return jsonify(all_ids)


@app.route('/points/read/<point>/<value>', methods=['GET'])
def name(point=None, value=None):
    global bacnet
    print(111, point, value)
    obj = bacnet.this_application.get_object_name(point)
    print(222, obj)
    print(3333, obj.units)
    obj.units = 'degreesCelsius'
    print(4444, obj.units)
    # value = executor.submit(process_read, bacnet, point)
    # res = value.result(2)
    return 'res'


if __name__ == '__main__':
    start()
