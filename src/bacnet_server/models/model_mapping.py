from mrb.mapper import api_to_topic_mapper
from mrb.message import Response, HttpMethod
from sqlalchemy.orm import validates

from src import db
from src.bacnet_server.models.model_base import ModelBase


class BPGPointMapping(ModelBase):
    __tablename__ = 'mappings_bp_gp'

    uuid = db.Column(db.String, primary_key=True)
    bacnet_point_uuid = db.Column(db.String(80), db.ForeignKey('bac_points.uuid'), nullable=False)
    generic_point_uuid = db.Column(db.String, nullable=False, unique=True)
    bacnet_point_name = db.Column(db.String(80), nullable=False)
    generic_point_name = db.Column(db.String(80), nullable=False)

    @validates('generic_point_uuid')
    def validate_generic_point_uuid(self, _, value):
        response: Response = api_to_topic_mapper(api=f'/api/generic/points/uuid/{value}',
                                                 destination_identifier='ps', http_method=HttpMethod.GET)
        if response.error:
            raise ValueError(response.error_message)
        return value

    @validates('generic_point_name')
    def validate_generic_point_name(self, _, value):
        if not value:
            raise ValueError('generic_point_name should not be null or blank')
        return value

    @validates('bacnet_point_name')
    def validate_bacnet_point_name(self, _, value):
        if not value:
            raise ValueError('bacnet_point_name should not be null or blank')
        return value

    @classmethod
    def find_by_bacnet_point_uuid(cls, bacnet_point_uuid):
        return cls.query.filter_by(bacnet_point_uuid=bacnet_point_uuid).first()

    @classmethod
    def find_by_generic_point_uuid(cls, generic_point_uuid):
        return cls.query.filter_by(generic_point_uuid=generic_point_uuid).first()
