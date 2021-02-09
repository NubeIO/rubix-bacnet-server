import copy

from flask_restful import abort, marshal_with, reqparse
from flask_restful.reqparse import request
from mrb.validator import is_bridge

from src.bacnet_server import BACServer
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.models.model_priority_array import PriorityArrayModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase


class BACnetPointSingular(BACnetPointBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('object_type', type=str, required=False)
    parser_patch.add_argument('object_name', type=str, required=False)
    parser_patch.add_argument('address', type=int, required=False)
    parser_patch.add_argument('relinquish_default', type=float, required=False)
    parser_patch.add_argument("priority_array_write", type=dict, required=False)
    parser_patch.add_argument('event_state', type=str, required=False)
    parser_patch.add_argument('units', type=str, required=False)
    parser_patch.add_argument('description', type=str, required=False)
    parser_patch.add_argument('enable', type=bool, required=False)
    parser_patch.add_argument('fault', type=bool, required=False)
    parser_patch.add_argument('data_round', type=int, required=False)
    parser_patch.add_argument('data_offset', type=float, required=False)

    @classmethod
    @marshal_with(point_fields)
    def get(cls, uuid):
        point = BACnetPointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message='BACnet Point is not found')
        return point

    @classmethod
    @marshal_with(point_fields)
    def patch(cls, uuid):
        data = BACnetPointSingular.parser_patch.parse_args()
        point = copy.deepcopy(BACnetPointModel.find_by_uuid(uuid))
        cls.abort_if_bacnet_is_not_running()
        if point is None:
            abort(404, message=f"Does not exist {uuid}")
        try:
            priority_array_write = data.pop('priority_array_write')
            non_none_data = {}
            for key in data.keys():
                if data[key] is not None:
                    non_none_data[key] = data[key]
            BACnetPointModel.filter_by_uuid(uuid).update(non_none_data)
            if priority_array_write:
                PriorityArrayModel.filter_by_point_uuid(uuid).update(priority_array_write)
            BACServer().remove_point(point)
            point_return = BACnetPointModel.find_by_uuid(uuid)
            BACServer().add_point(point_return, not is_bridge(request.args))
            return point_return
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def delete(cls, uuid):
        point = BACnetPointModel.find_by_uuid(uuid)
        if point:
            BACServer().remove_point(point)
            point.delete_from_db()
        return '', 204
