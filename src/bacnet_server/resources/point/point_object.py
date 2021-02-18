from src.bacnet_server.models.model_point import BACnetPointModel
from src.bacnet_server.resources.point.point_base_singular import BACnetPointBaseSingular


class BACnetPointObject(BACnetPointBaseSingular):

    @classmethod
    def get_point(cls, **kwargs) -> BACnetPointModel:
        return BACnetPointModel.find_by_object_id(kwargs.get('object_type'), kwargs.get('address'))
