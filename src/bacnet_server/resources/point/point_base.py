from flask_restful import reqparse
from rubix_http.exceptions.exception import BadDataException
from rubix_http.resource import RubixResource

from src.bacnet_server import BACServer
from src.bacnet_server.models.model_point import BACnetPointModel


class BACnetPointBase(RubixResource):
    parser = reqparse.RequestParser()
    parser.add_argument('object_type', type=str)
    parser.add_argument('object_name', type=str)
    parser.add_argument('use_next_available_address', type=bool)
    parser.add_argument('address', type=int)
    parser.add_argument('relinquish_default', type=float)
    parser.add_argument("priority_array_write", type=dict)
    parser.add_argument('event_state', type=str)
    parser.add_argument('units', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('enable', type=bool)
    parser.add_argument('fault', type=bool)
    parser.add_argument('data_round', type=int)
    parser.add_argument('data_offset', type=float)

    nested_priority_array_write_parser = reqparse.RequestParser()
    nested_priority_array_write_parser.add_argument('_1', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_2', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_3', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_4', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_5', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_6', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_7', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_8', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_9', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_10', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_11', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_12', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_13', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_14', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_15', type=float, location=('priority_array_write',))
    nested_priority_array_write_parser.add_argument('_16', type=float, location=('priority_array_write',))

    @classmethod
    def add_point(cls, data, uuid):
        priority_array_write: dict = data.pop('priority_array_write') or {}
        point = BACnetPointModel(uuid=uuid, **data)
        if point.use_next_available_address and point.address:
            raise BadDataException("address needs to be null when use_next_available_address is true")
        elif not point.use_next_available_address and not point.address:
            raise BadDataException("address cannot be null when use_next_available_address is false")
        point.save_to_db(priority_array_write)
        BACServer().add_point(point)
        return point

    @classmethod
    def abort_if_bacnet_is_not_running(cls):
        if not BACServer().status():
            raise BadDataException('BACnet server is not running')
