from flask_restful import fields

point_fields = {
    'uuid': fields.String,
    'object_identifier': fields.String,
    'object_type': fields.String,
    'object_name': fields.Integer,
    'address': fields.Integer,
    'present_value': fields.Float,
    'relinquish_default': fields.Float,
    'priority_array': fields.String,
    'units': fields.String,
    'description': fields.String,
    'enable': fields.Boolean,
    'fault': fields.Boolean,
    'data_round': fields.Integer,
    'data_offset': fields.Float,
    'created_on': fields.String,
    'updated_on': fields.String,
}
