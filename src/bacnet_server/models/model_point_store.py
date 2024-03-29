import json
import logging
from typing import List

import gevent
from flask import Response
from rubix_http.method import HttpMethod
from rubix_http.request import gw_request
from sqlalchemy import and_

from src import db
from src.bacnet_server.interfaces.mapping.mappings import MappingState
from src.bacnet_server.models.model_mapping import BPGPointMapping
from src.bacnet_server.models.model_priority_array import PriorityArrayModel

logger = logging.getLogger(__name__)


class BACnetPointStoreModel(db.Model):
    __tablename__ = 'bac_points_store'
    point_uuid = db.Column(db.String, db.ForeignKey('bac_points.uuid'), primary_key=True, nullable=False)
    present_value = db.Column(db.Float(), nullable=False)
    ts = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    @classmethod
    def find_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def create_new_point_store_model(cls, point_uuid):
        point = cls.find_by_point_uuid(point_uuid)
        pv = 0.0
        if point is not None:
            pv = point.relinquish_default
        return BACnetPointStoreModel(point_uuid=point_uuid, present_value=pv)

    def update(self) -> bool:
        res = db.session.execute(self.__table__
                                 .update()
                                 .values(present_value=self.present_value)
                                 .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                             self.__table__.c.present_value != self.present_value)))
        updated: bool = bool(res.rowcount)
        if updated:
            priority_array_write: dict = PriorityArrayModel.filter_by_point_uuid(self.point_uuid).first().to_dict()
            """BACnet > Generic point value"""
            self.__sync_point_value_bp_to_gp_process(priority_array_write)
            """BACnet > Modbus point value"""
            self.__sync_point_value_bp_to_mp_process(priority_array_write)
        return updated

    def sync_point_value_bp_to_mp(self, priority_array_write: dict):
        response: Response = gw_request(f"/ps/api/mappings/mp_gbp/bacnet/{self.point_uuid}")
        if response.status_code == 200:
            priority_array_write.pop('point_uuid', None)
            gw_request(
                api=f"/ps/api/modbus/points_value/uuid/{json.loads(response.data).get('modbus_point_uuid')}",
                body={"priority_array_write": priority_array_write},
                http_method=HttpMethod.PATCH
            )

    def __sync_point_value_bp_to_mp_process(self, priority_array_write: dict):
        gevent.spawn(self.sync_point_value_bp_to_mp, priority_array_write)

    @staticmethod
    def sync_point_value_bp_to_gp(mapped_point_uuid: str, priority_array_write: dict):
        priority_array_write.pop('point_uuid', None)
        gw_request(
            api=f"/ps/api/generic/points_value/uuid/{mapped_point_uuid}",
            body={"priority_array_write": priority_array_write},
            http_method=HttpMethod.PATCH
        )

    def __sync_point_value_bp_to_gp_process(self, priority_array_write: dict):
        mapping: BPGPointMapping = BPGPointMapping.find_by_point_uuid(self.point_uuid)
        if mapping and mapping.mapping_state == MappingState.MAPPED:
            gevent.spawn(self.sync_point_value_bp_to_gp, mapping.mapped_point_uuid, priority_array_write)

    @classmethod
    def sync_points_values_bp_to_gp_process(cls):
        mappings: List[BPGPointMapping] = BPGPointMapping.find_all()
        for mapping in mappings:
            if mapping.mapping_state == MappingState.MAPPED:
                point_store: BACnetPointStoreModel = BACnetPointStoreModel.find_by_point_uuid(mapping.point_uuid)
                if point_store:
                    point_store.__sync_point_value_bp_to_gp_process(point_store.point.priority_array_write.to_dict())
