from abc import abstractmethod

import shortuuid
from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.bacnet_server.interfaces.mapping.mappings import MappingState
from src.bacnet_server.models.model_mapping import BPGPointMapping
from src.bacnet_server.models.model_point_store import BACnetPointStoreModel
from src.bacnet_server.resources.model_fields import mapping_bp_gp_fields


def sync_point_value(mapping: BPGPointMapping):
    if mapping.mapping_state in (MappingState.MAPPED.name, MappingState.MAPPED):
        point_store: BACnetPointStoreModel = BACnetPointStoreModel.find_by_point_uuid(mapping.point_uuid)
        point_store.sync_point_value_bp_to_gp(mapping.mapped_point_uuid,
                                              point_store.point.priority_array_write.to_dict())
    return mapping


class BPGPMappingResourceList(RubixResource):
    @classmethod
    @marshal_with(mapping_bp_gp_fields)
    def get(cls):
        return BPGPointMapping.find_all()


class BPGPMappingResourceListByUUID(RubixResource):
    @classmethod
    @marshal_with(mapping_bp_gp_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('point_uuid', type=str, required=True)
        parser.add_argument('mapped_point_uuid', type=str, required=True)

        data = parser.parse_args()
        data.uuid = shortuuid.uuid()
        mapping: BPGPointMapping = BPGPointMapping(**data)
        mapping.save_to_db()
        sync_point_value(mapping)
        return mapping


class BPGPMappingResourceListByName(RubixResource):
    @classmethod
    @marshal_with(mapping_bp_gp_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('point_name', type=str, required=True)
        parser.add_argument('mapped_point_name', type=str, required=True)

        data = parser.parse_args()
        data.uuid = shortuuid.uuid()
        mapping: BPGPointMapping = BPGPointMapping(**data)
        mapping.save_to_db()
        sync_point_value(mapping)
        return mapping


class BPGPMappingResourceUpdateMappingState(RubixResource):
    @classmethod
    def get(cls):
        mappings = BPGPointMapping.find_all()
        for mapping in mappings:
            try:
                mapping.mapping_state = MappingState.MAPPED
                mapping.check_self()
            except ValueError:
                try:
                    mapping.set_uuid_with_name()
                except ValueError:
                    mapping.mapping_state = MappingState.BROKEN
            mapping.commit()
            sync_point_value(mapping)
        return {"message": "Mapping state has been updated successfully"}


class BPGPMappingResourceBase(RubixResource):
    @classmethod
    @marshal_with(mapping_bp_gp_fields)
    def get(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException('Does not exist {uuid}')
        return mapping

    @classmethod
    def delete(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException(f'Does not exist {uuid}')
        mapping.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_mapping(cls, uuid) -> BPGPointMapping:
        raise NotImplementedError


class BPGPMappingResourceByUUID(BPGPMappingResourceBase):
    parser = reqparse.RequestParser()
    parser.add_argument('point_uuid', type=str, required=True)
    parser.add_argument('mapped_point_uuid', type=str, required=True)

    @classmethod
    @marshal_with(mapping_bp_gp_fields)
    def patch(cls, uuid):
        data = BPGPMappingResourceByUUID.parser.parse_args()
        mapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException(f'Does not exist {uuid}')
        mapping.update(**data)
        sync_point_value(mapping)
        return mapping

    @classmethod
    def get_mapping(cls, uuid) -> BPGPointMapping:
        return BPGPointMapping.find_by_uuid(uuid)


class GBPMappingResourceByGenericPointUUID(BPGPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> BPGPointMapping:
        return BPGPointMapping.find_by_mapped_point_uuid(uuid)


class GBPMappingResourceByBACnetPointUUID(BPGPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> BPGPointMapping:
        return BPGPointMapping.find_by_point_uuid(uuid)
