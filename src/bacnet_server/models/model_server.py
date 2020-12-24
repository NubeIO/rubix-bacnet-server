import uuid

from src import db, BACnetSetting


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
    def create_default_server_if_does_not_exist(cls, config: BACnetSetting):
        bacnet_server = BACnetServerModel.find_one()
        if not bacnet_server:
            uuid_ = str(uuid.uuid4())
            bacnet_server = BACnetServerModel(uuid=uuid_,
                                              ip=config.ip,
                                              port=config.port,
                                              device_id=config.device_id,
                                              local_obj_name=config.local_obj_name,
                                              model_name=config.model_name,
                                              vendor_id=config.vendor_id,
                                              vendor_name=config.vendor_name)
            bacnet_server.save_to_db()
        return bacnet_server
