from flask_restful import Resource, reqparse, abort, marshal_with

from src.source_drivers.bacnet.models.device import BacnetDeviceModel
from src.source_drivers.bacnet.resources.fields import device_fields
from src.source_drivers.bacnet.services.device import Device as DeviceService


class Device(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('bac_device_mac',
                        type=int,
                        required=False,
                        help='BACnet mstp device bac_device_mac address'
                        )
    parser.add_argument('bac_device_id',
                        type=int,
                        required=True,
                        help='Every device needs a bacnet device id'
                        )
    parser.add_argument('bac_device_ip',
                        type=str,
                        required=True,
                        help='Every device needs a network bac_device_ip.'
                        )
    parser.add_argument('bac_device_mask',
                        type=int,
                        required=True,
                        help='Every device needs a network bac_device_mask'
                        )
    parser.add_argument('bac_device_port',
                        type=int,
                        required=True,
                        help='Every device needs a network bac_device_port'
                        )
    parser.add_argument('network_uuid',
                        type=str,
                        required=True,
                        help='Every device needs a network bac_device_uuid'
                        )

    @marshal_with(device_fields)
    def get(self, uuid):
        device = BacnetDeviceModel.find_by_bac_device_uuid(uuid)
        if not device:
            abort(404, message='Device not found.')
        return device

    @marshal_with(device_fields)
    def post(self, uuid):
        if BacnetDeviceModel.find_by_bac_device_uuid(uuid):
            return {'message': "An device with bac_device_uuid '{}' already exists.".format(uuid)}, 400
        data = Device.parser.parse_args()
        device = Device.create_device_model_obj(uuid, data)
        if device.find_by_bac_device_uuid(uuid) is not None:
            abort(409, message="Already exist this value")
        device.save_to_db()
        return device, 201

    @marshal_with(device_fields)
    def put(self, uuid):
        data = Device.parser.parse_args()
        device = BacnetDeviceModel.find_by_bac_device_uuid(uuid)
        if device is None:
            device = Device.create_device_model_obj(uuid, data)
        else:
            device.bac_device_mac = data['bac_device_mac']
            device.bac_device_id = data['bac_device_id']
            device.bac_device_ip = data['bac_device_ip']
            device.bac_device_mask = data['bac_device_mask']
            device.bac_device_port = data['bac_device_port']
            device.network_id = data['network_uuid']
        device.save_to_db()
        return device

    def delete(self, uuid):
        device = BacnetDeviceModel.find_by_bac_device_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204

    @staticmethod
    def create_device_model_obj(bac_device_uuid, data):
        return BacnetDeviceModel(bac_device_uuid=bac_device_uuid, bac_device_mac=data['bac_device_mac'],
                                 bac_device_id=data['bac_device_id'], bac_device_ip=data['bac_device_ip'],
                                 bac_device_mask=data['bac_device_mask'], bac_device_port=data['bac_device_port'],
                                 network_uuid=data['network_uuid'])


class DeviceList(Resource):
    @marshal_with(device_fields, envelope="devices")
    def get(self):
        return BacnetDeviceModel.query.all()


class DevicePoints(Resource):
    def get(self, dev_uuid):
        response = {}
        device = BacnetDeviceModel.find_by_bac_device_uuid(dev_uuid)
        if not device:
            abort(404, message='Device Not found')
        response['network_uuid'] = device.network.network_uuid
        response['bac_device_uuid'] = device.bac_device_uuid
        response['bac_device_mac'] = device.bac_device_mac
        try:
            response['points'] = DeviceService.get_instance().get_points(device)
        except Exception as e:
            abort(500, message=str(e))
        return response


class DevicePoint(Resource):
    def get(self, dev_uuid, obj, obj_instance, prop):
        response = {}
        device = BacnetDeviceModel.find_by_bac_device_uuid(dev_uuid)
        if not device:
            abort(404, message='Device Not found')
        response['network_uuid'] = device.network.network_uuid
        response['bac_device_uuid'] = device.bac_device_uuid
        response['bac_device_mac'] = device.bac_device_mac
        response['pnt_type'] = obj
        response['pnt_id'] = obj_instance
        try:
            response['point'] = DeviceService.get_instance().get_point(device, obj, obj_instance, prop)
        except Exception as e:
            abort(500, message=str(e))

        return response
