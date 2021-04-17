def to_bool(value):
    if value == True:
        return True
    elif not value:
        return False
    else:
        return {"True": True, "true": True}.get(value, False)

