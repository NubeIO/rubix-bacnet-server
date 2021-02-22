from rubix_http.resource import RubixResource

from src.bacnet_server.models.model_point_store import BACnetPointStoreModel


class BPGPSync(RubixResource):

    @classmethod
    def get(cls):
        BACnetPointStoreModel.sync_points_values()
