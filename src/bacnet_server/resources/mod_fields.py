from flask_restful import fields

point_store_fields = {
    'point_uuid': fields.String,
    'object_identifier': fields.Float,
    'present_value': fields.String,
    'priority_array': fields.Boolean,
    'ts': fields.String
}

point_fields = {
    'uuid': fields.String,
    'object_type': fields.String,
    'object_name': fields.String,
    'address': fields.Integer,
    'relinquish_default': fields.Float,
    'priority_array_write': fields.String,
    'units': fields.String,
    'description': fields.String,
    'enable': fields.Boolean,
    'fault': fields.Boolean,
    'data_round': fields.Integer,
    'data_offset': fields.Float,
    'created_on': fields.String,
    'updated_on': fields.String,
    'point_store': fields.Nested(point_store_fields)
}
