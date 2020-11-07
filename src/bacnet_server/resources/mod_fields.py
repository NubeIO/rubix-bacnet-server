from flask_restful import fields

point_fields = {
    'uuid': fields.String,
    'name': fields.String,
    'reg': fields.Integer,
    'reg_length': fields.Integer,
    'type': fields.String,
    'enable': fields.Boolean,
    'write_value': fields.Float,
    'data_type': fields.String,
    'data_endian': fields.String,
    'data_round': fields.Integer,
    'data_offset': fields.Integer,
    'timeout': fields.Integer,
    'timeout_global': fields.Boolean,
    'prevent_duplicates': fields.Boolean,
    'prevent_duplicates_global': fields.Boolean,
    'created_on': fields.String,
    'updated_on': fields.String,
    'device_uuid': fields.String,
}
