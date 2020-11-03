from server_v2.breakdowns.helper_point_array import highest_priority
from server_v2.breakdowns.server_debug import _debug_points


def point_save(pnt_dict, object_identifier, object_name, object_type,
               present_value, _type, old_value, new_value, db, Points):
    _priority_array = pnt_dict.get("priorityArray")
    highest_priority_array = highest_priority(_priority_array, _type)
    priority_value = None
    priority_pri_value = None
    if highest_priority_array is not None:
        priority_value = highest_priority_array[0]
        priority_pri_value = highest_priority_array[1]
    else:
        priority_value = priority_value
        priority_pri_value = priority_pri_value

    if _debug_points:
        print({"object_identifier": object_identifier,
               "object_name": object_name,
               "object_type": object_type,
               "_priority_array": _priority_array,
               "priority_value": priority_value,
               "priority_pri_value": priority_pri_value,
               "present_value": present_value, 'old_value': old_value,
               'new_value': new_value})

    insert_if_none = db.search(Points.object_identifier == object_identifier)
    if not insert_if_none:
        db.insert({"object_identifier": object_identifier,
                   "object_name": object_name,
                   "object_type": object_type,
                   "_priority_array": _priority_array,
                   "highest_priority_array": highest_priority_array,
                   "priority_value": priority_value,
                   "priority_pri_value": priority_pri_value,
                   "present_value": present_value})
    else:
        db.update({
            "_priority_array": _priority_array,
            "highest_priority_array": highest_priority_array,
            "priority_value": priority_value,
            "priority_pri_value": priority_pri_value,
            "present_value": present_value,
        }, Points.object_identifier == object_identifier)
