import copy

from flask_restful import abort, marshal_with

from src.bacnet_server.bac_server import BACServer
from src.bacnet_server.helpers.helper_mqtt import publish_mqtt_value
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.models.model_priority_array import PriorityArrayModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase


class BACnetPointSingular(BACnetPointBase):
    """
    It returns point with point_store object value, which has the current values of point_store for that particular
    point with last not null value and value_array
    """

    @marshal_with(point_fields)
    def get(self, uuid):
        point = BACnetPointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message='BACnet Point is not found')
        return point

    @marshal_with(point_fields)
    def put(self, uuid):
        data = BACnetPointSingular.parser.parse_args()
        point = copy.deepcopy(BACnetPointModel.find_by_uuid(uuid))
        if point is None:
            return self.add_point(data, uuid)
        try:
            priority_array_write = data.pop('priority_array_write')
            BACnetPointModel.filter_by_uuid(uuid).update(data)
            PriorityArrayModel.filter_by_point_uuid(uuid).update(priority_array_write)
            BACnetPointModel.commit()
            BACServer.get_instance().remove_point(point)
            point_return = BACnetPointModel.find_by_uuid(uuid)
            [object_identifier, present_value] = BACServer.get_instance().add_point(point_return)
            publish_mqtt_value(object_identifier, present_value)
            return point_return
        except Exception as e:
            abort(500, message=str(e))

    def delete(self, uuid):
        point = BACnetPointModel.find_by_uuid(uuid)
        if point:
            BACServer.get_instance().remove_point(point)
            point.delete_from_db()
        return '', 204
