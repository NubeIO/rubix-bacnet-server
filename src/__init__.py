import os
from threading import Thread

import BAC0
import paho.mqtt.client as mqtt
from bacpypes.basetypes import EngineeringUnits, PriorityArray
from bacpypes.local.object import AnalogOutputCmdObject
from bacpypes.primitivedata import CharacterString, Real
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from src.bacnet_server.breakdowns.helper_point_array import create_object_identifier, default_values
from src.bacnet_server.config import NetworkConfig, PointConfig

# from src.modbus.services.point_store_cleaner import PointStoreCleaner

app = Flask(__name__)
CORS(app)

db_pg = False
if db_pg:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/bac_rest"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20
    }
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

db = SQLAlchemy(app)
from src import routes

db.create_all()


def mqtt_start():
    global client
    client = mqtt.Client()
    client.loop_start()
    try:
        client.connect("0.0.0.0", 1883, 60)
        client.loop_forever()
    except Exception as e:
        print(f"Error {e}")


class AnalogOutputFeedbackObject(AnalogOutputCmdObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._property_monitors["presentValue"].append(self.check_feedback)

    def check_feedback(self, old_value, new_value):
        pnt_dict = self._dict_contents()
        object_identifier = create_object_identifier(self.objectIdentifier)
        object_name = self.objectName
        object_type = self.objectType
        present_value = self.presentValue
        if isinstance(present_value, Real):
            present_value = float(present_value.value)
        elif type(present_value) is float:
            present_value = float(present_value)
        _type = "real"
        topic = f"bacnet/server/points/ao/{object_identifier}"

        payload = str(present_value)
        print({'MQTT_PUBLISH': "MQTT_PUBLISH", 'topic': topic, 'payload': payload})
        # client.publish(topic, payload, qos=1, retain=True)
        client.publish(topic, payload, qos=1, retain=True)


def start_bac():
    global bacnet
    bacnet = None
    ip = NetworkConfig.ip
    port = NetworkConfig.port
    device_id = NetworkConfig.deviceId
    local_obj_name = NetworkConfig.localObjName

    ao_count = PointConfig.ao_count
    bacnet = BAC0.lite(ip=ip, port=port, deviceId=device_id, localObjName=local_obj_name)
    for i in range(1, int(ao_count) + 1):
        default_pv = 0.0
        object_type = 'analogOutput'
        # [priority_array, present_value] = default_values(object_type, i, default_pv)
        ao = AnalogOutputFeedbackObject(
            objectIdentifier=(object_type, i),
            objectName='analogOutput-%d' % (i,),
            presentValue=default_pv,
            eventState="normal",
            statusFlags=[0, 0, 0, 0],
            relinquishDefault=0.0,
            priorityArray=PriorityArray(),
            units=EngineeringUnits("milliseconds"),
            description=CharacterString("Sets fade time between led colors (0-32767)"),
        )
        bacnet.this_application.add_object(ao)


if not os.environ.get("WERKZEUG_RUN_MAIN"):
    mqtt_thread = Thread(target=mqtt_start, daemon=True)
    mqtt_thread.start()
    start_bac()
