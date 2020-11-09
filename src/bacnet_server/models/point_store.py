from src import db


class BACnetPointStoreModel(db.Model):
    __tablename__ = 'bac_points_store'
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    object_identifier = db.Column(db.String(80), nullable=False)
    present_value = db.Column(db.Float(), nullable=False)
    priority_array = db.Column(db.String())
    ts = db.Column(db.DateTime, server_default=db.func.now())
    point_uuid = db.Column(db.String, db.ForeignKey('bac_points.uuid'), nullable=False)

    def __repr__(self):
        return f"BACnetPointStore({self.id})"

    @classmethod
    def find_last_valid_row(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid, fault=False).order_by(cls.ts.desc()).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
