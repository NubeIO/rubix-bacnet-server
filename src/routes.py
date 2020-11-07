from flask_restful import Api
from src import app
from src.bacnet_server.resources.point.point_plural import BACnetPointPlural
from src.bacnet_server.resources.point.point_singular import BACnetPointSingular
from src.system.resources.memory import GetSystemMem


api_prefix = 'api'
api = Api(app)


api.add_resource(BACnetPointPlural, f'/{api_prefix}/modbus/points')
api.add_resource(BACnetPointSingular, f'/{api_prefix}/modbus/points/<string:uuid>')


api.add_resource(GetSystemMem, f'/{api_prefix}/system/memory')
