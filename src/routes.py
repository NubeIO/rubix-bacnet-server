from flask_restful import Api

from src import app
from src.bacnet_server.resources.point.point_name import BACnetPointName
from src.bacnet_server.resources.point.point_object import BACnetPointObject
from src.bacnet_server.resources.point.point_plural import BACnetPointPlural
from src.bacnet_server.resources.point.point_singular import BACnetPointSingular
from src.bacnet_server.resources.server.server import BACnetServer
from src.system.resources.ping import Ping

api_prefix = 'api'
api = Api(app)

api.add_resource(BACnetServer, f'/{api_prefix}/bacnet/server')
api.add_resource(BACnetPointPlural, f'/{api_prefix}/bacnet/points')
api.add_resource(BACnetPointSingular, f'/{api_prefix}/bacnet/points/uuid/<string:uuid>')
api.add_resource(BACnetPointObject, f'/{api_prefix}/bacnet/points/obj/<string:object_type>/<string:address>')
api.add_resource(BACnetPointName, f'/{api_prefix}/bacnet/points/name/<string:object_name>')
api.add_resource(Ping, f'/{api_prefix}/system/ping')


from src.bacnet_master.resources.device import Device, DeviceList, DevicePoints, DevicePoint, PointWritePresentValue
from src.bacnet_master.resources.network import Network, NetworkList, NetworksIds

bacnet_api_prefix = f'{api_prefix}/bac/master/'
api.add_resource(Device, f'/{bacnet_api_prefix}/dev/<string:uuid>')
api.add_resource(Network, f'/{bacnet_api_prefix}/network/<string:uuid>')
api.add_resource(DeviceList, f'/{bacnet_api_prefix}/devices')
api.add_resource(DevicePoints, f'/{bacnet_api_prefix}/points/objects/<string:dev_uuid>')
# get a point /dev_uuid/analogInput/1/85
api.add_resource(DevicePoint, f'/{bacnet_api_prefix}/point/read/<string:dev_uuid>/<string:obj>/<string:obj_instance>/<string:prop>')
api.add_resource(NetworkList, f'/{bacnet_api_prefix}/networks')
api.add_resource(NetworksIds, f'/{bacnet_api_prefix}/networks/ids')

api.add_resource(PointWritePresentValue, f'/{bacnet_api_prefix}/point/write/<string:dev_uuid>/<string:obj>/<string:obj_instance>/<string:value>')
