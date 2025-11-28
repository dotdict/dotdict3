class DotDict(dict):
    def __init__(self, d):
        for k, v in d.items():
            self[k] = v

    def __setitem__(self, k, v):
        return super().__setitem__(k, _convert(v))

    __delattr__ = dict.__delitem__
    __getattr__ = dict.__getitem__
    __setattr__ = __setitem__


class DotList(list):
    def __init__(self, l):
        for i in l:
            self.append(i)

    def append(self, object):
        return super().append(_convert(object))

    def insert(self, index, object):
        return super().insert(index, _convert(object))


def _convert(object):
    if isinstance(object, dict) and not isinstance(object, DotDict):
        return DotDict(object)
    if isinstance(object, (tuple, list, set, range)) and not isinstance(object, DotList):
        return DotList(object)
    return object
