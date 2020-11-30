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
api.add_resource(Ping, f'/{api_prefix}/ping')
