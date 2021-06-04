import json

from flask import Response
from rubix_http.request import gw_request

from src import db
from src.bacnet_server.interfaces.mapping.mappings import MappingState
from src.bacnet_server.models.model_base import ModelBase


class BPGPointMapping(ModelBase):
    __tablename__ = 'mappings_bp_gp'

    uuid = db.Column(db.String, primary_key=True)
    point_uuid = db.Column(db.String(80), db.ForeignKey('bac_points.uuid'), nullable=False)
    mapped_point_uuid = db.Column(db.String, nullable=False, unique=True)
    point_name = db.Column(db.String(80), nullable=False)
    mapped_point_name = db.Column(db.String(80), nullable=False)
    mapping_state = db.Column(db.Enum(MappingState), default=MappingState.MAPPED)

    def check_self(self) -> (bool, any):
        super().check_self()
        if self.point_uuid:
            self.__set_point_name()
        if self.mapped_point_uuid:
            self.__set_mapped_point_name()
        if not self.point_uuid:
            self.__set_point_uuid()
        if not self.mapped_point_uuid:
            self.__set_mapped_point_uuid()

    def __set_point_name(self):
        from src.bacnet_server.models.model_point import BACnetPointModel
        if not self.point_uuid:
            raise ValueError(f"point_uuid should not be null or blank")
        point: BACnetPointModel = BACnetPointModel.find_by_uuid(self.point_uuid)
        if not point:
            raise ValueError(f"Does not exist point_uuid {self.point_uuid}")
        self.point_name = point.object_name

    def __set_mapped_point_name(self):
        if not self.mapped_point_uuid:
            raise ValueError(f"mapped_point_uuid should not be null or blank")
        response: Response = gw_request(f'/ps/api/generic/points/uuid/{self.mapped_point_uuid}')
        if response.status_code != 200:
            raise ValueError(f"Does not exist mapped_point_uuid {self.mapped_point_uuid}")
        self.mapped_point_name = json.loads(response.data).get('name')

    def __set_point_uuid(self):
        from src.bacnet_server.models.model_point import BACnetPointModel
        if not self.point_name:
            raise ValueError("point name should not be null or blank")
        point: BACnetPointModel = BACnetPointModel.find_by_object_name(self.point_name)
        if not point:
            raise ValueError(f"Does not exist point_name {self.point_name}")
        self.point_uuid = point.uuid

    def __set_mapped_point_uuid(self):
        if not self.mapped_point_name:
            raise ValueError("mapped_point_name should not be null or blank")
        mapped_point_names = self.mapped_point_name.split(":")
        if len(mapped_point_names) != 3:
            raise ValueError("mapped_point_names should be colon (:) delimited network_name:device_name:point_name")
        network_name, device_name, point_name = mapped_point_names
        response: Response = gw_request(f'/ps/api/generic/points/name/{network_name}/{device_name}/{point_name}')
        if response.status_code != 200:
            raise ValueError(f"Does not exit mapped_point_name {self.mapped_point_name}")
        self.mapped_point_uuid = json.loads(response.data).get('uuid')

    @classmethod
    def find_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def find_by_mapped_point_uuid(cls, mapped_point_uuid):
        return cls.query.filter_by(mapped_point_uuid=mapped_point_uuid).first()
