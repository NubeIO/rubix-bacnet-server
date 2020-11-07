from src import db
# from src.modbus.interfaces.point.points import ModbusPointType, ModbusDataType, ModbusDataEndian
from src.bacnet_server.interfaces.point.points import ModbusPointType, ModbusDataEndian, ModbusDataType


class BACnetPointModel(db.Model):
    __tablename__ = 'bac_points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    reg = db.Column(db.Integer(), nullable=False)
    reg_length = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Enum(ModbusPointType), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    write_value = db.Column(db.Float(), nullable=False)
    data_type = db.Column(db.Enum(ModbusDataType), nullable=False)
    data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False)
    data_round = db.Column(db.Integer(), nullable=False)
    data_offset = db.Column(db.String(80), nullable=False)
    timeout = db.Column(db.Integer(), nullable=False)
    timeout_global = db.Column(db.Boolean(), nullable=False)
    prevent_duplicates = db.Column(db.Boolean(), nullable=False)
    prevent_duplicates_global = db.Column(db.Boolean(), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


    def __repr__(self):
        return f"BACnetPointModel({self.uuid})"

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def filter_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def commit(cls):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
