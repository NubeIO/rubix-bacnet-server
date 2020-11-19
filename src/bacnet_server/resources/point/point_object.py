from flask_restful import marshal_with, abort

from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase


class BACnetPointObject(BACnetPointBase):
    @marshal_with(point_fields)
    def get(self, object_type, address):
        point = BACnetPointModel.find_by_object_id(object_type, address)
        if not point:
            abort(404, message='BACnet Point is not found')
        return point
