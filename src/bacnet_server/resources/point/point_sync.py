from flask_restful import Resource

from src.bacnet_server.models.model_point_store import BACnetPointStoreModel


class BPGPSync(Resource):

    @classmethod
    def get(cls):
        BACnetPointStoreModel.sync_points_values()
