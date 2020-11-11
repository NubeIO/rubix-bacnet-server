import uuid

from flask_restful import marshal_with

from src.bacnet_server.models.point import BACnetPointModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase


class BACnetPointPlural(BACnetPointBase):
    @marshal_with(point_fields, envelope="points")
    def get(self):
        return BACnetPointModel.query.all()

    @marshal_with(point_fields)
    def post(self):
        _uuid = str(uuid.uuid4())
        data = BACnetPointPlural.parser.parse_args()
        data.priority_array_write = str(data.priority_array_write)
        return self.add_point(data, _uuid)
