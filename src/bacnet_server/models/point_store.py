from src import db


class ModbusPointStoreModel(db.Model):
    __tablename__ = 'mod_points_store'
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    value = db.Column(db.Float(), nullable=False)
    value_array = db.Column(db.String())
    fault = db.Column(db.Boolean(), default=False, nullable=False)
    fault_message = db.Column(db.String())
    ts = db.Column(db.DateTime, server_default=db.func.now())
    point_uuid = db.Column(db.String, db.ForeignKey('mod_points.uuid'), nullable=False)

    def __repr__(self):
        return f"ModbusPointStore({self.id})"

    @classmethod
    def find_last_valid_row(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid, fault=False).order_by(cls.ts.desc()).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
