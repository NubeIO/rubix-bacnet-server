from src import db


class BacnetDeviceModel(db.Model):
    __tablename__ = 'bacnet_devices'
    device_name = db.Column(db.String(80), unique=False, nullable=False)
    device_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    device_mac = db.Column(db.Integer(), unique=False, nullable=False)
    device_id = db.Column(db.Integer(), unique=False, nullable=False)
    device_ip = db.Column(db.String(80), unique=False, nullable=False)
    device_mask = db.Column(db.Integer(), nullable=False)
    device_port = db.Column(db.Integer(), nullable=False)
    type_mstp = db.Column(db.Boolean())
    network_uuid = db.Column(db.String, db.ForeignKey('bacnet_networks.network_uuid'))
    network_number = db.Column(db.Integer())

    def __repr__(self):
        return f"Device(device_uuid = {self.network_uuid})"

    @classmethod
    def find_by_device_uuid(cls, device_uuid):
        return cls.query.filter_by(device_uuid=device_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
