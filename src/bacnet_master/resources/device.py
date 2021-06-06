import logging

from flask_restful import Resource, reqparse, abort, marshal_with

from src.bacnet_master.models.device import BacnetDeviceModel
from src.bacnet_master.resources.fields import device_fields
from src.bacnet_master.services.device import Device as DeviceService

logger = logging.getLogger(__name__)


class Device(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('device_name',
                        type=str,
                        required=False,
                        help='BACnet mstp device device_mac address'
                        )
    parser.add_argument('device_mac',
                        type=int,
                        required=False,
                        help='BACnet mstp device device_mac address'
                        )
    parser.add_argument('device_id',
                        type=int,
                        required=True,
                        help='Every device needs a bacnet device id'
                        )
    parser.add_argument('device_ip',
                        type=str,
                        required=False,
                        help='Every device needs a network device_ip.'
                        )
    parser.add_argument('device_mask',
                        type=int,
                        required=False,
                        help='Every device needs a network device_mask'
                        )
    parser.add_argument('device_port',
                        type=int,
                        required=False,
                        help='Every device needs a network device_port'
                        )
    parser.add_argument('network_uuid',
                        type=str,
                        required=True,
                        help='Every device needs a network device_uuid'
                        )
    parser.add_argument('type_mstp',
                        type=bool,
                        required=False,
                        help='True if device is type MSTP'
                        )
    parser.add_argument('network_number',
                        type=int,
                        required=False,
                        help='Used for discovering networking (set to 0 to disable)'
                        )

    @marshal_with(device_fields)
    def get(self, uuid):
        device = BacnetDeviceModel.find_by_device_uuid(uuid)
        if not device:
            abort(404, message='Device not found.')
        return device

    @marshal_with(device_fields)
    def post(self, uuid):
        if BacnetDeviceModel.find_by_device_uuid(uuid):
            return {'message': "An device with device_uuid '{}' already exists.".format(uuid)}, 400
        data = Device.parser.parse_args()
        device = Device.create_device_model_obj(uuid, data)
        if device.find_by_device_uuid(uuid) is not None:
            abort(409, message="Already exist this value")
        device.save_to_db()
        return device, 201

    @marshal_with(device_fields)
    def put(self, uuid):
        data = Device.parser.parse_args()
        device = BacnetDeviceModel.find_by_device_uuid(uuid)
        if device is None:
            device = Device.create_device_model_obj(uuid, data)
        else:
            device.device_name = data['device_name']
            device.device_mac = data['device_mac']
            device.device_id = data['device_id']
            device.device_ip = data['device_ip']
            device.device_mask = data['device_mask']
            device.device_port = data['device_port']
            device.network_id = data['network_uuid']
            device.network_number = data['network_number']
            device.type_mstp = data['type_mstp']
        device.save_to_db()
        return device

    def delete(self, uuid):
        device = BacnetDeviceModel.find_by_device_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204

    @staticmethod
    def create_device_model_obj(device_uuid, data):
        return BacnetDeviceModel(device_uuid=device_uuid, device_name=data['device_name'],
                                 device_mac=data['device_mac'],
                                 device_id=data['device_id'], device_ip=data['device_ip'],
                                 device_mask=data['device_mask'], device_port=data['device_port'],
                                 network_uuid=data['network_uuid'], network_number=data['network_number'],
                                 type_mstp=data['type_mstp'])


class DeviceList(Resource):
    @marshal_with(device_fields, envelope="devices")
    def get(self):
        return BacnetDeviceModel.query.all()


class DeviceObjectList(Resource):
    def get(self, dev_uuid):
        response = {}
        device = BacnetDeviceModel.find_by_device_uuid(dev_uuid)
        if not device:
            abort(404, message='Device Not found')
        response['network_uuid'] = device.network.network_uuid
        response['device_uuid'] = device.device_uuid
        response['device_mac'] = device.device_mac
        try:
            response['points'] = DeviceService.get_instance().get_object_list(device)
        except Exception as e:
            abort(500, message=str(e))
        return response


class PointWritePresentValue(Resource):
    def get(self, dev_uuid, obj, obj_instance, value, priority):
        response = {}
        device = BacnetDeviceModel.find_by_device_uuid(dev_uuid)
        if not device:
            abort(404, message='Device Not found')
        response['network_uuid'] = device.network.network_uuid
        response['device_uuid'] = device.device_uuid
        response['device_mac'] = device.device_mac
        response['pnt_type'] = obj
        response['pnt_id'] = obj_instance
        try:
            response['point'] = DeviceService().write_point_present_value(device, obj, obj_instance, value, priority)
        except Exception as e:
            abort(500, message=str(e))
        return response


class BuildPointsList(Resource):
    def get(self, dev_uuid):
        device = BacnetDeviceModel.find_by_device_uuid(dev_uuid)
        if not device:
            abort(404, message='Points not found')
        read = DeviceService.get_instance().read_point_list(device)
        if not read:
            abort(404, message='Cant read point')
        return {
            "points": read
        }
