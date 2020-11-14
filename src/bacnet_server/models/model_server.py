import uuid

from src import db
from src.ini_config import config


class BACnetServerModel(db.Model):
    __tablename__ = 'bac_server'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    ip = db.Column(db.String(80), nullable=False)
    port = db.Column(db.Integer(), nullable=False)
    device_id = db.Column(db.String(80), nullable=False)
    local_obj_name = db.Column(db.String(80), nullable=False)
    model_name = db.Column(db.String(80), nullable=False)
    vendor_id = db.Column(db.String(80), nullable=False)
    vendor_name = db.Column(db.String(80), nullable=False)

    @classmethod
    def find_one(cls):
        return cls.query.first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create_default_server_if_does_not_exist(cls):
        ip = config.get('device', 'ip')
        port = config.get('device', 'port')
        device_id = config.get('device', 'device_id')
        local_obj_name = config.get('device', 'local_obj_name')
        model_name = config.get('device', 'model_name')
        vendor_id = config.get('device', 'vendor_id')
        vendor_name = config.get('device', 'vendor_name')

        bacnet_server = BACnetServerModel.find_one()
        if not bacnet_server:
            uuid_ = str(uuid.uuid4())
            bacnet_server = BACnetServerModel(uuid=uuid_,
                                              ip=ip,
                                              port=port,
                                              device_id=device_id,
                                              local_obj_name=local_obj_name,
                                              model_name=model_name,
                                              vendor_id=vendor_id,
                                              vendor_name=vendor_name)
            bacnet_server.save_to_db()
        return bacnet_server
