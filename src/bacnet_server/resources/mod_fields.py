from flask_restful import fields

point_fields = {
    '''
     object_identifier: str, unique, feedback from bacpypes, This is made up of a combination of the `object_type` and `address`, Example: analogOutput-1
     present_value: will be the result of the highest priority_array. so for example as below the present_value: 22.2 
     units: megawattHoursReactive
     object_type: analogOutput
     priority_array_write: {
    "_1": 22.2,
    "_2": "None",
    "_3": "None",
    "_4": "None",
    "_5": "None",
    "_6": "None",
    "_7": "None",
    "_8": "None",
    "_9": "None",
    "_10": "None",
    "_11": "None",
    "_12": "None",
    "_13": "None",
    "_14": "None", None is send no data but dont change the priority array
    "_15": "NULL", THIS WILL LET THE USER SEND A null to realise the value from @15
    "_16": 99
},
    '''
    
    'uuid': fields.String,
    'object_identifier': fields.String,
    'object_type': fields.String,
    'object_name': fields.String,
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
