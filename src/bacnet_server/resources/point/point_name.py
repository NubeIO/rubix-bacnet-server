import copy

from flask_restful import marshal_with, abort, reqparse

from src.bacnet_server.bac_server import BACServer
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.models.model_priority_array import PriorityArrayModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase


class BACnetPointName(BACnetPointBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('object_name', type=str, required=False)
    parser_patch.add_argument('relinquish_default', type=float, required=False)
    parser_patch.add_argument("priority_array_write", type=dict, required=False)
    parser_patch.add_argument('event_state', type=str, required=False)
    parser_patch.add_argument('units', type=str, required=False)
    parser_patch.add_argument('description', type=str, required=False)
    parser_patch.add_argument('enable', type=bool, required=False)
    parser_patch.add_argument('fault', type=bool, required=False)
    parser_patch.add_argument('data_round', type=int, required=False)
    parser_patch.add_argument('data_offset', type=float, required=False)

    @marshal_with(point_fields)
    def get(self, object_name):
        point = BACnetPointModel.find_by_object_name(object_name)
        if not point:
            abort(404, message='BACnet Point is not found')
        return point

    @marshal_with(point_fields)
    def patch(self, object_name):
        data = BACnetPointName.parser_patch.parse_args()
        point = copy.deepcopy(BACnetPointModel.find_by_object_name(object_name))
        if point is None:
            abort(404, message=f"Does not exist {object_name}")
        try:
            priority_array_write = data.pop('priority_array_write')
            non_none_data = {}
            for key in data.keys():
                if data[key] is not None:
                    non_none_data[key] = data[key]
            if priority_array_write:
                PriorityArrayModel.filter_by_point_uuid(point.uuid).update(priority_array_write)
            BACnetPointModel.filter_by_uuid(point.uuid).update(non_none_data)
            BACServer.get_instance().remove_point(point)
            point_return = BACnetPointModel.find_by_uuid(point.uuid)
            BACServer.get_instance().add_point(point_return)
            return point_return
        except Exception as e:
            abort(500, message=str(e))


