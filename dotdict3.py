__version__ = "1.0.0"


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, d={}):
        for k, v in d.items():
            self[k] = v

    def __setitem__(self, k, v):
        if isinstance(v, dict):
            return dict.__setitem__(self, k, DotDict(v))
        elif isinstance(v, (list, tuple)):
            return dict.__setitem__(self, k, DotList(v))
        else:
            return dict.__setitem__(self, k, v)


class DotList(list):
    def __init__(self, l):
        for x in l:
            if isinstance(x, dict):
                self.append(DotDict(x))
            elif isinstance(x, (list, tuple)):
                self.append(DotList(x))
            else:
                self.append(x)
