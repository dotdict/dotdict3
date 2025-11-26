class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, d):
        for k, v in d.items():
            self[k] = v

    def __setitem__(self, k, v):
        if isinstance(v, dict) and not isinstance(v, DotDict):
            return super().__setitem__(k, DotDict(v))
        elif isinstance(v, (tuple, list, set, range)):
            return super().__setitem__(k, DotList(v))
        return super().__setitem__(k, v)


class DotList(list):
    def __init__(self, l):
        for i in l:
            self.append(i)

    def append(self, i):
        if isinstance(i, dict) and not isinstance(i, DotDict):
            super().append(DotDict(i))
        elif isinstance(i, (tuple, list, set, range)) and not isinstance(i, DotList):
            super().append(DotList(i))
        else:
            super().append(i)
