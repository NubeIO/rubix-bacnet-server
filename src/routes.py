from flask_restful import Api
from src import app
from src.bacnet_server.resources.point.point_plural import ModbusPointPlural
from src.bacnet_server.resources.point.point_singular import ModbusPointSingular
from src.system.resources.memory import GetSystemMem


api_prefix = 'api'
api = Api(app)


api.add_resource(ModbusPointPlural, f'/{api_prefix}/modbus/points')
api.add_resource(ModbusPointSingular, f'/{api_prefix}/modbus/points/<string:uuid>')


api.add_resource(GetSystemMem, f'/{api_prefix}/system/memory')
