import uuid

from flask_restful import marshal_with

from src.bacnet_server import BACServer
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase


class BACnetPointPlural(BACnetPointBase):
    @marshal_with(point_fields, envelope="points")
    def get(self):
        return BACnetPointModel.query.all()

    @marshal_with(point_fields)
    def post(self):
        self.abort_if_bacnet_is_not_running()
        _uuid = str(uuid.uuid4())
        data = BACnetPointPlural.parser.parse_args()
        return self.add_point(data, _uuid)

    def delete(self):
        BACnetPointModel.delete_all_from_db()
        BACServer().remove_all_points()
        return '', 204
