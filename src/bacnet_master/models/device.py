from src import db


class BacnetDeviceModel(db.Model):
    __tablename__ = 'bacnet_devices'
    bac_device_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    bac_device_mac = db.Column(db.Integer(), unique=False, nullable=False)
    bac_device_id = db.Column(db.Integer(), unique=False, nullable=False)
    bac_device_ip = db.Column(db.String(20), unique=False, nullable=False)
    bac_device_mask = db.Column(db.Integer(), nullable=False)
    bac_device_port = db.Column(db.Integer(), nullable=False)
    network_uuid = db.Column(db.String, db.ForeignKey('bacnet_networks.network_uuid'))

    def __repr__(self):
        return f"Device(bac_device_uuid = {self.network_uuid})"

    @classmethod
    def find_by_bac_device_uuid(cls, bac_device_uuid):
        return cls.query.filter_by(bac_device_uuid=bac_device_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
