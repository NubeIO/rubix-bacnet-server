from rubix_http.resource import RubixResource

from src.background import Background
from src.bacnet_server.models.model_point_store import BACnetPointStoreModel


class BPToGPSync(RubixResource):

    @classmethod
    def get(cls):
        BACnetPointStoreModel.sync_points_values_bp_to_gp_process()


class MPSync(RubixResource):
    @classmethod
    def get(cls):
        Background.sync_on_start()
