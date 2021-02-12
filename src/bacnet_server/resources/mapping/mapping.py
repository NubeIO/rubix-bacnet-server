from flask_restful import Resource, marshal_with, reqparse, abort
from sqlalchemy.exc import IntegrityError

from src.bacnet_server.models.model_mapping import BPGPointMapping
from src.bacnet_server.resources.model_fields import bp_gp_mapping_fields


class BPGPMappingResourceList(Resource):
    @classmethod
    @marshal_with(bp_gp_mapping_fields)
    def get(cls):
        return BPGPointMapping.find_all()

    @classmethod
    @marshal_with(bp_gp_mapping_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('bacnet_point_uuid', type=str, required=True)
        parser.add_argument('generic_point_uuid', type=str, required=True)
        parser.add_argument('bacnet_point_name', type=str, required=True)
        parser.add_argument('generic_point_name', type=str, required=True)
        try:
            data = parser.parse_args()
            mapping = BPGPointMapping(**data)
            mapping.save_to_db()
            return mapping
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))


class BPGPMappingResourceBase(Resource):
    @classmethod
    @marshal_with(bp_gp_mapping_fields)
    def get(cls, point_uuid):
        mapping = cls.get_mapping(point_uuid)
        if not mapping:
            abort(404, message=f'Does not exist {point_uuid}')
        return mapping

    @classmethod
    def delete(cls, point_uuid):
        mapping = cls.get_mapping(point_uuid)
        if mapping is None:
            abort(404, message=f'Does not exist {point_uuid}')
        else:
            mapping.delete_from_db()
        return '', 204


class GBPMappingResourceByGenericPointUUID(BPGPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return BPGPointMapping.find_by_generic_point_uuid(point_uuid)


class GBPMappingResourceByBACnetPointUUID(BPGPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return BPGPointMapping.find_by_bacnet_point_uuid(point_uuid)
