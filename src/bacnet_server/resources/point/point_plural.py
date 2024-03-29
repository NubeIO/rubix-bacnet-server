import shortuuid
from flask_restful import marshal_with

from src.bacnet_server import BACServer
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.resources.model_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase


class BACnetPointPlural(BACnetPointBase):
    @classmethod
    @marshal_with(point_fields)
    def get(cls):
        return BACnetPointModel.find_all()

    @classmethod
    @marshal_with(point_fields)
    def post(cls):
        data = BACnetPointPlural.parser.parse_args()
        return cls.add_point(data, shortuuid.uuid())

    @classmethod
    def delete(cls):
        BACnetPointModel.delete_all_from_db()
        if BACServer().status():
            BACServer().remove_all_points()
        return '', 204
