from flask_restful import Resource, reqparse, abort

from src.bacnet_server.models.point import BACnetPointModel


class BACnetPointBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('object_type', type=str, required=False)
    parser.add_argument('object_name', type=str, required=False)
    parser.add_argument('address', type=int, required=False)
    parser.add_argument("priority_array_write", type=str, required=False)
    parser.add_argument('relinquish_default', type=float, required=False)
    parser.add_argument('units', type=str, required=False)
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('enable', type=bool, required=False)
    parser.add_argument('fault', type=bool, required=False)
    parser.add_argument('data_round', type=int, required=False)
    parser.add_argument('data_offset', type=float, required=False)

    def add_point(self, data, uuid):
        try:
            point = BACnetPointModel(uuid=uuid, **data)
            point.save_to_db()
            return point
        except Exception as e:
            abort(500, message=str(e))
