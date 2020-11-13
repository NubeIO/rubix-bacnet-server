#TODO remove

# from tinydb import TinyDB, Query
#
# from src.bacnet_server.config import DbConfig, PointConfig
# from src.bacnet_server.helpers.helper_point_array import create_object_identifier
#
# db_location = DbConfig.location
# db_name = DbConfig.name
# db_file = f'{db_location}/{db_name}.json'
# db = TinyDB(db_file)
# Points = Query()
#
# ao_count = PointConfig.ao_count
# bo_count = PointConfig.bo_count
# default_pv = 'inactive'
# object_type = 'binaryOutput'
# for i in range(1, int(bo_count) + 1):
#     point_obj = {
#         'object_identifier': create_object_identifier(object_type, i),
#         'object_name': create_object_identifier(object_type, i),
#         'present_value': default_pv,
#         'event_state': 'normal',
#         'status_flags': [0, 0, 0, 0],
#         'feedback_value': 'inactive',
#         'relinquish_default': 'inactive',
#         '_priority_array': None,
#         'highest_priority_array': None,
#         'priority_value': None,
#         'description': f'{object_type} {i}',
#     }
#     db.insert(point_obj)
#
# default_pv = 0.0
# object_type = 'analogOutput'
# for i in range(1, int(ao_count) + 1):
#     point_obj = {
#         'object_identifier': create_object_identifier(object_type, i),
#         'object_name': create_object_identifier(object_type, i),
#         'present_value': default_pv,
#         'event_state': 'normal',
#         'status_flags': [0, 0, 0, 0],
#         'relinquish_default': default_pv,
#         '_priority_array': None,
#         'highest_priority_array': None,
#         'priority_value': None,
#         'units': 'milliseconds',
#         'description': f'{object_type} {i}',
#     }
#     print(point_obj)
#     db.insert(point_obj)
