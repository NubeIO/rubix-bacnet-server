from flask_restful import Resource, reqparse, abort
from src.bacnet_server.models.point import BACnetPointModel


class BACnetPointBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('object_identifier', type=str, required=False)
    parser.add_argument('object_type', type=str, required=False)
    parser.add_argument('object_name', type=str, required=False)
    parser.add_argument('address', type=int, required=False)
    parser.add_argument('present_value', type=float, required=False)
    parser.add_argument("priority_array", type=str, required=False)
    parser.add_argument('relinquish_default', type=float, required=False)
    parser.add_argument('units', type=str, required=False)
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('enable', type=bool, required=False)
    parser.add_argument('fault', type=bool, required=False)
    parser.add_argument('data_round', type=int, required=False)
    parser.add_argument('data_offset', type=float, required=False)


    @staticmethod
    def create_point_model_obj(uuid, data):
        return BACnetPointModel(uuid=uuid, **data)

    def add_point(self, data, uuid):
        # self.abort_if_device_does_not_exist(data.device_uuid)
        try:
            point = BACnetPointBase.create_point_model_obj(uuid, data)
            point.save_to_db()
            return point
        except Exception as e:
            abort(500, message=str(e))



    def create_point_store(self, row):
        if row:
            return {
                'present_value': row.value,
                'priority_array': row.value_array,
                'ts': str(row.ts) if row.ts else None,
            }
        else:
            return {
                'present_value': None,
                'priority_array': None,
                'ts': None,
            }
