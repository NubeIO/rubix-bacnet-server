from bacpypes.basetypes import PriorityArray, PriorityValue


def create_object_identifier(obj):
    return "-".join(str(v) for v in obj)


def highest_priority(iterable, _type, default=None):
    if iterable:
        priority = 0
        for value in iterable:
            priority += 1
            val = value.get(_type)
            if val is not None:
                return [val, priority]
    return default


def default_values(object_type, i, default_pv, DB, Points):
    [priority_array, present_value] = get_priority_array_and_present_value(object_type, i, default_pv, DB, Points)
    if priority_array is None:
        priority_array = PriorityArray(),
    if present_value is None:
        present_value = default_pv
    return [priority_array, present_value]


def get_priority_array_and_present_value(identifier, i, default_pv, DB, Points):
    point = DB.search(Points.object_identifier == create_object_identifier((identifier, i)))
    priority_array = PriorityArray()
    present_value = default_pv
    if point and len(point) and point[0].get('_priority_array'):
        # convert `[{"null": []}, ...` to `[{"null": ()}, ...`
        _priority_array = point[0].get('_priority_array')
        _priority_array_temp = map(lambda x: {'null': ()} if 'null' in x.keys() else x, _priority_array)
        _priority_array = list(_priority_array_temp)
        for j in range(16):
            priority_array.__setitem__(j + 1, PriorityValue(**_priority_array[j]))
    if point and len(point) and point[0].get('present_value'):
        present_value = point[0].get('present_value')
    return [priority_array, present_value]
