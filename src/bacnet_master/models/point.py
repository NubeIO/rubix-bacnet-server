from src import db
from src.bacnet_master.interfaces.device import ObjType


class BacnetPointModel(db.Model):
    __tablename__ = 'bacnet_points'
    point_name = db.Column(db.String(80), unique=False, nullable=False)
    point_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    point_obj_id = db.Column(db.Integer(), unique=False, nullable=False)
    point_obj_type = db.Column(db.Enum(ObjType), unique=False, nullable=False)
    device_uuid = db.Column(db.String, db.ForeignKey('bacnet_devices.device_uuid'))

    def __repr__(self):
        return f"Device(point_uuid = {self.device_uuid})"

    @classmethod
    def find_by_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
