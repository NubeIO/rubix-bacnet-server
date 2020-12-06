from flask_restful import Resource, reqparse, fields, marshal_with, abort

from src.source_drivers.bacnet.models.network import BacnetNetworkModel
from src.source_drivers.bacnet.resources.fields import network_fields
from src.source_drivers.bacnet.services.network import Network as NetworkService


class Network(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('network_ip',
                        type=str,
                        required=True,
                        help='network_ip must be a string'
                        )
    parser.add_argument('network_mask',
                        type=int,
                        required=True,
                        help='netmask must be an int length 2'
                        )
    parser.add_argument('network_port',
                        type=int,
                        required=True,
                        help='network_port must must be an int length 4'
                        )
    parser.add_argument('network_number',
                        type=int,
                        required=True,
                        help='bacnet network number must must be an int'
                        )
    parser.add_argument('network_device_id',
                        type=int,
                        required=True,
                        help='bacnet id is needed'
                        )
    parser.add_argument('network_device_name',
                        type=str,
                        required=True,
                        help='bacnet device name is needed'
                        )

    @marshal_with(network_fields)
    def get(self, uuid):
        network = BacnetNetworkModel.find_by_network_uuid(uuid)
        if not network:
            abort(404, message='Network not found')
        return network

    @marshal_with(network_fields)
    def post(self, uuid):
        if BacnetNetworkModel.find_by_network_uuid(uuid):
            return abort(409, message=f"An Network with network_uuid '{uuid}' already exists.")
        data = Network.parser.parse_args()
        network = Network.create_network_model_obj(uuid, data)
        network.save_to_db()
        NetworkService.get_instance().add_network(network)
        return network, 201

    @marshal_with(network_fields)
    def put(self, uuid):
        data = Network.parser.parse_args()
        network = BacnetNetworkModel.find_by_network_uuid(uuid)
        if network is None:
            network = Network.create_network_model_obj(uuid, data)
        else:
            network.network_ip = data['network_ip']
            network.network_mask = data['network_mask']
            network.network_port = data['network_port']
            network.network_number = data['network_number']
            network.network_device_id = data['network_device_id']
            network.network_device_name = data['network_device_name']
        network.save_to_db()
        NetworkService.get_instance().add_network(network)
        return network, 201

    def delete(self, uuid):
        network_uuid = uuid
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if network:
            network.delete_from_db()
            NetworkService.get_instance().delete_network(network)
        return '', 204

    @staticmethod
    def create_network_model_obj(network_uuid, data):
        return BacnetNetworkModel(network_uuid=network_uuid, network_ip=data['network_ip'], network_mask=data['network_mask'],
                                  network_port=data['network_port'], network_device_id=data['network_device_id'],
                                  network_device_name=data['network_device_name'], network_number=data['network_number'])


class NetworkList(Resource):
    @marshal_with(network_fields, envelope="networks")
    def get(self):
        return BacnetNetworkModel.query.all()


class NetworksIds(Resource):
    @marshal_with({'network_uuid': fields.String}, envelope="networks")
    def get(self):
        return BacnetNetworkModel.query.all()
