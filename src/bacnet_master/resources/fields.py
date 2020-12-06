from flask_restful import fields

device_fields = {
    'bac_device_uuid': fields.String,
    'bac_device_mac': fields.Integer,
    'bac_device_id': fields.Integer,
    'bac_device_ip': fields.String,
    'bac_device_mask': fields.Integer,
    'bac_device_port': fields.Integer,
    'network_uuid': fields.String,
}

network_fields = {
    'network_uuid': fields.String,
    'network_ip': fields.String,
    'network_mask': fields.Integer,
    'network_port': fields.Integer,
    'network_device_id': fields.Integer,
    'network_device_name': fields.String,
    'network_number': fields.Integer,
    'devices': fields.List(fields.Nested(device_fields))
}
