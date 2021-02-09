from flask_restful import Resource, abort

from src.bacnet_server.helpers.helper_point_store import sync_to_point_server
from src.bacnet_server.models.model_point import BACnetPointModel


class BACnetPointSync(Resource):

    @classmethod
    def get(cls, uuid):
        point: BACnetPointModel = BACnetPointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message=f"point {uuid} not found")
        sync_to_point_server(point.uuid, point.point_store.present_value, True)
        return {}
