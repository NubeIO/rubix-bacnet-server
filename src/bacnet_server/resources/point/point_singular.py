import copy
from abc import abstractmethod

from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException, BadDataException

from src.bacnet_server import BACServer
from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.models.model_priority_array import PriorityArrayModel
from src.bacnet_server.resources.model_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase


class BACnetPointSingular(BACnetPointBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('object_type', type=str, required=False)
    parser_patch.add_argument('object_name', type=str, required=False)
    parser_patch.add_argument('use_next_available_address', type=bool, required=False)
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
    def get(cls, **kwargs):
        point: BACnetPointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('BACnet Point is not found')
        return point

    @classmethod
    @marshal_with(point_fields)
    def patch(cls, **kwargs):
        data = cls.parser_patch.parse_args()
        point: BACnetPointModel = copy.deepcopy(cls.get_point(**kwargs))
        cls.abort_if_bacnet_is_not_running()
        if point is None:
            raise NotFoundException(f"Does not exist with {kwargs}")
        use_next_available_address: bool = data.get('use_next_available_address')
        address: str = data.get('address')
        if use_next_available_address is not None or address is not None:
            if use_next_available_address is None:
                use_next_available_address = point.use_next_available_address
            if use_next_available_address and address:
                raise BadDataException("address needs to be null when use_next_available_address is true")
            elif not use_next_available_address and not address:
                raise BadDataException("address cannot be null when use_next_available_address is false")

        priority_array_write = data.pop('priority_array_write')
        non_none_data = {}
        for key in data.keys():
            if data[key] is not None:
                non_none_data[key] = data[key]
        if priority_array_write:
            PriorityArrayModel.filter_by_point_uuid(point.uuid).update(priority_array_write)
        BACnetPointModel.filter_by_uuid(point.uuid).update(non_none_data)
        BACServer().remove_point(point)
        point_return = BACnetPointModel.find_by_uuid(point.uuid)
        BACServer().add_point(point_return)
        return point_return

    @classmethod
    def delete(cls, **kwargs):
        point: BACnetPointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException(f'Not found {kwargs}')
        BACServer().remove_point(point)
        point.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> BACnetPointModel:
        raise NotImplementedError


class BACnetPointSingularByUUID(BACnetPointSingular):
    @classmethod
    def get_point(cls, **kwargs) -> BACnetPointModel:
        return BACnetPointModel.find_by_uuid(kwargs.get('uuid'))


class BACnetPointSingularByObject(BACnetPointSingular):
    @classmethod
    def get_point(cls, **kwargs) -> BACnetPointModel:
        return BACnetPointModel.find_by_object_id(kwargs.get('object_type'), kwargs.get('address'))


class BACnetPointSingularByName(BACnetPointSingular):
    @classmethod
    def get_point(cls, **kwargs) -> BACnetPointModel:
        return BACnetPointModel.find_by_object_name(kwargs.get('object_name'))
