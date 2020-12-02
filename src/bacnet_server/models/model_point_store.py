from sqlalchemy import and_, or_

from src import db


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

    def update(self) -> bool:
        res = db.session.execute(self.__table__
                                 .update()
                                 .values(present_value=self.present_value)
                                 .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                             or_(self.__table__.c.present_value != self.present_value))))
        return bool(res.rowcount)
