from sqlalchemy import inspect

from src import db
from src.bacnet_server.helpers.helper_point_array import dict_priority


class PriorityArrayModel(db.Model):
    __tablename__ = 'priority_array'
    point_uuid = db.Column(db.String, db.ForeignKey('bac_points.uuid'), primary_key=True, nullable=False)
    _1 = db.Column(db.Float(), nullable=True)
    _2 = db.Column(db.Float(), nullable=True)
    _3 = db.Column(db.Float(), nullable=True)
    _4 = db.Column(db.Float(), nullable=True)
    _5 = db.Column(db.Float(), nullable=True)
    _6 = db.Column(db.Float(), nullable=True)
    _7 = db.Column(db.Float(), nullable=True)
    _8 = db.Column(db.Float(), nullable=True)
    _9 = db.Column(db.Float(), nullable=True)
    _10 = db.Column(db.Float(), nullable=True)
    _11 = db.Column(db.Float(), nullable=True)
    _12 = db.Column(db.Float(), nullable=True)
    _13 = db.Column(db.Float(), nullable=True)
    _14 = db.Column(db.Float(), nullable=True)
    _15 = db.Column(db.Float(), nullable=True)
    _16 = db.Column(db.Float(), nullable=True)

    def __repr__(self):
        return f"PriorityArray(point_uuid = {self.point_uuid})"

    @classmethod
    def create_new_point_store_model(cls, point_uuid):
        return PriorityArrayModel(point_uuid=point_uuid)

    @classmethod
    def filter_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid)

    @classmethod
    def get_priority_by_point_uuid(cls, point_uuid):
        x = cls.query.filter_by(point_uuid=point_uuid).first()
        return dict_priority(x)

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
