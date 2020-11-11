from flask_restful import fields

point_store_fields = {
    'point_uuid': fields.String,
    'object_identifier': fields.Float,
    'present_value': fields.String,
    'priority_array': fields.Boolean,
    'ts': fields.String
}

priority_array_write_fields = {
    '_1': fields.Float,
    '_2': fields.Float,
    '_3': fields.Float,
    '_4': fields.Float,
    '_5': fields.Float,
    '_6': fields.Float,
    '_7': fields.Float,
    '_8': fields.Float,
    '_9': fields.Float,
    '_10': fields.Float,
    '_11': fields.Float,
    '_12': fields.Float,
    '_13': fields.Float,
    '_14': fields.Float,
    '_15': fields.Float,
    '_16': fields.Float,
}

point_fields = {
    'uuid': fields.String,
    'object_type': fields.String,
    'object_name': fields.String,
    'address': fields.Integer,
    'relinquish_default': fields.Float,
    'priority_array_write': fields.Nested(priority_array_write_fields),
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
