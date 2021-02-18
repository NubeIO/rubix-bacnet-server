from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.resources.point.point_base_singular import BACnetPointBaseSingular


class BACnetPointSingular(BACnetPointBaseSingular):

    @classmethod
    def get_point(cls, **kwargs) -> BACnetPointModel:
        return BACnetPointModel.find_by_uuid(kwargs.get('uuid'))
