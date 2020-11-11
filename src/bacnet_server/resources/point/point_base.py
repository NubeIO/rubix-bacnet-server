from flask_restful import Resource, reqparse, abort

from src.bacnet_server.models.model_point import BACnetPointModel


class BACnetPointBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('object_type', type=str)
    parser.add_argument('object_name', type=str)
    parser.add_argument('address', type=int)
    parser.add_argument("priority_array_write", type=dict)
    parser.add_argument('relinquish_default', type=float)
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

    def add_point(self, data, uuid):
        try:
            priority_array_write = data.pop('priority_array_write')
            point = BACnetPointModel(uuid=uuid, **data)
            point.save_to_db(priority_array_write)
            return point
        except Exception as e:
            abort(500, message=str(e))
