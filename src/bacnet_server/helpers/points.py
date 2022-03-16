def encode_binary_present_value(value):
    return "active" if value else "inactive"


def decode_binary_present_value(value):
    if value == "active":
        return 1
    elif value == "inactive":
        return 0


def type_to_mqtt_topic(value):
    if value == "analogOutput":
        return "ao"
    elif value == "analogValue":
        return "av"
    elif value == "binaryOutput":
        return "bo"
    elif value == "binaryValue":
        return "bv"
