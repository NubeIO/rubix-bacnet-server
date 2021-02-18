from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.resources.point.point_base_singular import BACnetPointBaseSingular


class BACnetPointName(BACnetPointBaseSingular):

    @classmethod
    def get_point(cls, **kwargs) -> BACnetPointModel:
        return BACnetPointModel.find_by_object_name(kwargs.get('object_name'))
