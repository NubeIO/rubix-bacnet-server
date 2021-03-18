from flask_restful import reqparse, marshal_with
from rubix_http.resource import RubixResource

from src import db
from src.bacnet_server.bac_server import BACServer
from src.bacnet_server.models.model_server import BACnetServerModel
from src.bacnet_server.resources.model_fields import server_field


class BACnetServer(RubixResource):
    parser = reqparse.RequestParser()
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('device_id', type=str)
    parser.add_argument('local_obj_name', type=str)
    parser.add_argument('model_name', type=str)
    parser.add_argument('vendor_id', type=str)
    parser.add_argument('vendor_name', type=str)

    @classmethod
    @marshal_with(server_field)
    def get(cls):
        return BACnetServerModel.find_one()

    @classmethod
    @marshal_with(server_field)
    def patch(cls):
        data = BACnetServer.parser.parse_args()
        data_to_update = {}
        for key in data.keys():
            if data[key] is not None:
                data_to_update[key] = data[key]
        BACnetServerModel.find_one().update(**data_to_update)
        new_bacnet_server = BACnetServerModel.find_one()
        BACServer().restart_bac(new_bacnet_server)
        db.session.commit()
        return new_bacnet_server
