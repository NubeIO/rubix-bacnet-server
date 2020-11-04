from tinydb import TinyDB, Query

from server.breakdowns.helper_point_array import default_values
from server.config import DbConfig, PointConfig

db_location = DbConfig.location
db_name = DbConfig.name
# db_file = 'test_db.json'
db_file = f'{db_location}/{db_name}.json'
db = TinyDB(db_file)
Points = Query()

ao_count = PointConfig.ao_count
bo_count = PointConfig.bo_count
default_pv = 'inactive'
object_type = 'binaryOutput'
for i in range(1, int(bo_count) + 1):
    [priority_array, _present_value] = default_values(object_type, i, default_pv, db, Points)
    print(vars(priority_array))
    point_obj = {
        'object_identifier': f'{object_type} {i}',
        'object_type': f'{object_type}',
        'present_value': _present_value,
        'event_state': 'normal',
        'status_flags': [0, 0, 0, 0],
        'feedback_value': 'inactive',
        'relinquish_default': 'inactive',
        '_priority_array': None,
        'highest_priority_array': None,
        'priority_value': None,
        'description': f'{object_type} {i}',
    }
    db.insert(point_obj)

default_pv = 0.0
object_type = 'analogOutput'
for i in range(1, int(ao_count) + 1):
    [priority_array, _present_value] = default_values(object_type, i, default_pv, db, Points)
    print(vars(priority_array))
    point_obj = {
        'object_identifier': f'{object_type} {i}',
        'object_type': f'{object_type}',
        'present_value': _present_value,
        'event_state': 'normal',
        'status_flags': [0, 0, 0, 0],
        'relinquish_default': default_pv,
        '_priority_array': None,
        'highest_priority_array': None,
        'priority_value': None,
        'units': 'milliseconds',
        'description': f'{object_type} {i}',
    }
    db.insert(point_obj)
