from flask import Blueprint
from flask_restful import Api

from src.bacnet_server.resources.mapping.mapping import BPGPMappingResourceList, GBPMappingResourceByGenericPointUUID, \
    GBPMappingResourceByBACnetPointUUID
from src.bacnet_server.resources.point.point_name import BACnetPointName
from src.bacnet_server.resources.point.point_object import BACnetPointObject
from src.bacnet_server.resources.point.point_plural import BACnetPointPlural
from src.bacnet_server.resources.point.point_singular import BACnetPointSingular
from src.bacnet_server.resources.point.point_sync import BPGPSync
from src.bacnet_server.resources.server.server import BACnetServer
from src.system.resources.ping import Ping

bp_bacnet_server = Blueprint('bacnet_server', __name__, url_prefix='/api/bacnet')
api_bacnet_server = Api(bp_bacnet_server)

api_bacnet_server.add_resource(BACnetServer, '/server')
api_bacnet_server.add_resource(BACnetPointPlural, '/points')
api_bacnet_server.add_resource(BACnetPointSingular, '/points/uuid/<string:uuid>')
api_bacnet_server.add_resource(BACnetPointObject, '/points/obj/<string:object_type>/<string:address>')
api_bacnet_server.add_resource(BACnetPointName, '/points/name/<string:object_name>')

# BACnet points <> Generic points mappings
bp_bp_gp_mapping = Blueprint('bp_gp_mappings', __name__, url_prefix='/api/bp_gp/mappings')
api_bp_gp_mapping = Api(bp_bp_gp_mapping)
api_bp_gp_mapping.add_resource(BPGPMappingResourceList, '')
api_bp_gp_mapping.add_resource(GBPMappingResourceByBACnetPointUUID, '/bacnet/<string:point_uuid>')
api_bp_gp_mapping.add_resource(GBPMappingResourceByGenericPointUUID, '/generic/<string:point_uuid>')

bp_bp_gp_sync = Blueprint('bp_gp_sync', __name__, url_prefix='/api/bp_gp/sync')
api_bp_gp_sync = Api(bp_bp_gp_sync)
api_bp_gp_sync.add_resource(BPGPSync, '')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
