from bacpypes.basetypes import PriorityArray, PriorityValue


def create_object_identifier(object_type, address):
    return f'{object_type}-{address}'


def dict_priority(priority_array):
    priority_array_dict = {}
    for i in range(16):
        pri = f"_{i + 1}"
        _dict = priority_array.__dict__.get(pri)
        key = {pri: _dict}
        priority_array_dict.update(key)
    return priority_array_dict


def serialize_priority_array(priority_array):
    priority_array_dict = {}
    for i in range(16):
        priority_array_dict[f'_{i + 1}'] = None if list(priority_array[i].keys())[0] == 'null' else \
            list(priority_array[i].values())[0]
    return priority_array_dict


def get_highest_priority_field(priority_array):
    for i in range(17):
        value = getattr(priority_array, f'_{i + 1}', None)
        if value is not None:
            return i
    return 16


def highest_priority(iterable, _type, default=None):
    if iterable:
        priority = 0
        for value in iterable:
            priority += 1
            val = value.get(_type)
            if val is not None:
                return [val, priority]
    return default


def default_values(priority_array, default_pv):
    priority_array_return = PriorityArray()
    present_value = default_pv
    for i in range(16, 0, -1):
        value = getattr(priority_array, f'_{i}')
        if value is None:
            write = {'null': ()}
        else:
            present_value = value
            # TODO: Switch cases for different type of points
            write = {'real': value}
        priority_array_return.__setitem__(i, PriorityValue(**write))
    return [priority_array_return, present_value]


def default_values_binary(priority_array, default_pv):
    priority_array_return = PriorityArray()
    present_value = default_pv
    for i in range(16, 0, -1):
        value = getattr(priority_array, f'_{i}')
        if value is None:
            write = {'null': ()}
        else:
            present_value = value
            # TODO: Switch cases for different type of points
            write = {'enumerated': value != 0}
        priority_array_return.__setitem__(i, PriorityValue(**write))
    return [priority_array_return, present_value]
