from typing import List

from mrb.brige import MqttRestBridge
from mrb.mapper import api_to_topic_mapper
from mrb.message import HttpMethod
from sqlalchemy import and_, or_

from src import db, FlaskThread
from src.bacnet_server.models.model_mapping import BPGPointMapping


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
        return BACnetPointStoreModel(point_uuid=point_uuid, present_value=0)

    def update(self, sync: bool = True) -> bool:
        res = db.session.execute(self.__table__
                                 .update()
                                 .values(present_value=self.present_value)
                                 .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                             or_(self.__table__.c.present_value != self.present_value))))
        updated: bool = bool(res.rowcount)
        if MqttRestBridge.status() and updated and sync:
            FlaskThread(target=self.__sync_point_value, daemon=True).start()
        return updated

    def sync_point_value_with_mapping(self, mapping: BPGPointMapping):
        if not MqttRestBridge.status():
            return
        api_to_topic_mapper(
            api=f"/api/generic/points_value/uuid/{mapping.generic_point_uuid}",
            destination_identifier='ps',
            body={"value": self.present_value},
            http_method=HttpMethod.PATCH)

    def __sync_point_value(self):
        mapping: BPGPointMapping = BPGPointMapping.find_by_bacnet_point_uuid(self.point_uuid)
        if mapping:
            self.sync_point_value_with_mapping(mapping)

    @classmethod
    def sync_points_values(cls):
        if not MqttRestBridge.status():
            return
        mappings: List[BPGPointMapping] = BPGPointMapping.find_all()
        for mapping in mappings:
            point_store: BACnetPointStoreModel = BACnetPointStoreModel.find_by_point_uuid(mapping.bacnet_point_uuid)
            if point_store:
                FlaskThread(target=point_store.__sync_point_value, daemon=True).start()
