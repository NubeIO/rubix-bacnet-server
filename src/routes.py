from flask_restful import Api

from src import app
from src.bacnet_server.resources.point.point_plural import BACnetPointPlural
from src.bacnet_server.resources.point.point_singular import BACnetPointSingular
from src.bacnet_server.resources.server.server import BACnetServer
from src.bacnet_server.resources.server.server_status import BACnetServerStatus
from src.system.resources.ping import Ping

api_prefix = 'api'
api = Api(app)

api.add_resource(BACnetServer, f'/{api_prefix}/bacnet/server')
api.add_resource(BACnetServerStatus, f'/{api_prefix}/bacnet/server/status')
api.add_resource(BACnetPointPlural, f'/{api_prefix}/bacnet/points')
api.add_resource(BACnetPointSingular, f'/{api_prefix}/bacnet/points/<string:uuid>')
api.add_resource(Ping, f'/{api_prefix}/ping')
