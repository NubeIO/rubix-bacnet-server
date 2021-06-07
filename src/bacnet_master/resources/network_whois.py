import logging
from flask_restful import Resource, reqparse

from src.bacnet_master.interfaces.bacnet_calls import BACnetCommon
from src.bacnet_master.resources.device import Device
from src.bacnet_master.services.device import Device as DeviceService

logger = logging.getLogger(__name__)


class NetworkWhois(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('network_number',
                        type=int,
                        required=False,
                        help='network number'
                        )
    parser.add_argument('whois',
                        type=bool,
                        required=False,
                        help='if true do a whois, if false do a network discover'
                        )
    parser.add_argument('global_broadcast',
                        type=bool,
                        required=False,
                        help='global broadcast'
                        )
    parser.add_argument('full_range',
                        type=bool,
                        required=False,
                        help='WhoIs full range'
                        )
    parser.add_argument('range_start',
                        type=int,
                        required=False,
                        help='WhoIs looking for devices in the ID range EXAMPLE: START 10 (10 - 1000)'
                        )
    parser.add_argument('range_end',
                        type=int,
                        required=False,
                        help='WhoIs looking for devices in the ID range (10 - 1000) EXAMPLE: END 1000'
                        )


class Whois(Resource):
    def post(self, net_uuid):
        data = NetworkWhois.parser.parse_args()
        network_number = data['network_number']
        whois = data['whois']
        global_broadcast = data['global_broadcast']
        full_range = data['full_range']
        range_start = data['range_start']
        range_end = data['range_end']
        return DeviceService().whois(net_uuid, whois=whois,
                                     network_number=network_number,
                                     global_broadcast=global_broadcast,
                                     full_range=full_range,
                                     range_start=range_start,
                                     range_end=range_end)


class NetworkUnknownDeviceObjects(Resource):
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


class UnknownDeviceObjects(Resource):
    def post(self, net_uuid):
        data = NetworkUnknownDeviceObjects.parser.parse_args()
        device_id = data['device_id']
        device_ip = data['device_ip']
        device_mac = data['device_mac']
        device_mask = data['device_mask']
        device_port = data['device_port']
        type_mstp = data['type_mstp']
        network_number = data['network_number']
        device = {
            "device_id": device_id,
            "device_ip": device_ip,
            "device_mac": device_mac,
            "device_mask": device_mask,
            "device_port": device_port,
            "type_mstp": type_mstp,
            "network_number": network_number
        }
        # url = DeviceService.build_url(device_ip=device_ip, device_mask=device_mask, device_port=device_port)
        return DeviceService().unknown_get_object_list(net_uuid, device)
