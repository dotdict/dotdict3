class DotDict(dict):
    def __init__(self, data):
        for key, value in data.items():
            self[key] = value

    def __setitem__(self, key, value):
        return super().__setitem__(key, _convert(value))

    __delattr__ = dict.__delitem__
    __getattr__ = dict.__getitem__
    __setattr__ = __setitem__


class DotList(list):
    def __init__(self, items):
        for item in items:
            self.append(item)

    def append(self, items):
        return super().append(_convert(items))

    def insert(self, index, items):
        return super().insert(index, _convert(items))


def _convert(obj):
    if isinstance(obj, dict) and not isinstance(obj, DotDict):
        return DotDict(obj)
    if isinstance(obj, list) and not isinstance(obj, DotList):
        return DotList(obj)
    return obj
