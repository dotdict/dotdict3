class DotDict(dict):
    def __init__(self, object):
        for key, value in object.items():
            self[key] = value

    def __setitem__(self, key, value):
        return super().__setitem__(key, _convert(value))

    __delattr__ = dict.__delitem__
    __getattr__ = dict.__getitem__
    __setattr__ = __setitem__


class DotList(list):
    def __init__(self, object):
        for item in object:
            self.append(item)

    def append(self, object):
        return super().append(_convert(object))

    def insert(self, index, object):
        return super().insert(index, _convert(object))


def _convert(object):
    if isinstance(object, dict) and not isinstance(object, DotDict):
        return DotDict(object)
    if isinstance(object, list) and not isinstance(object, DotList):
        return DotList(object)
    return object
