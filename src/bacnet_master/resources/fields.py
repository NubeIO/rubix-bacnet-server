from flask_restful import fields

device_fields = {
    'device_name': fields.String,
    'device_uuid': fields.String,
    'device_mac': fields.Integer,
    'device_id': fields.Integer,
    'device_ip': fields.String,
    'device_mask': fields.Integer,
    'device_port': fields.Integer,
    'network_uuid': fields.String,
    'network_number': fields.Integer,
    'type_mstp': fields.Boolean
}

network_fields = {
    'network_name': fields.String,
    'network_uuid': fields.String,
    'network_ip': fields.String,
    'network_mask': fields.Integer,
    'network_port': fields.Integer,
    'network_device_id': fields.Integer,
    'network_device_name': fields.String,
    'devices': fields.List(fields.Nested(device_fields))
}

point_fields = {
    'point_name': fields.String,
    'point_uuid': fields.String,
    'point_obj_id': fields.Integer,
    'point_obj_type': fields.String,
    'device_uuid': fields.String,
}
