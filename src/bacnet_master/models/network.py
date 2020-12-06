from src import db


class BacnetNetworkModel(db.Model):
    __tablename__ = 'bacnet_networks'
    network_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    network_ip = db.Column(db.String(20), unique=False, nullable=False)
    network_mask = db.Column(db.Integer(), nullable=False)
    network_port = db.Column(db.Integer(), nullable=False)
    network_device_id = db.Column(db.Integer(), nullable=False)
    network_device_name = db.Column(db.String(80), nullable=False)
    network_number = db.Column(db.Integer())
    devices = db.relationship('BacnetDeviceModel', cascade="all,delete", backref='network', lazy=True)

    def __repr__(self):
        return f"Network(network_uuid = {self.network_uuid})"

    @classmethod
    def find_by_network_uuid(cls, network_uuid):
        return cls.query.filter_by(network_uuid=network_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
