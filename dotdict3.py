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
        for x in l:
            if isinstance(x, dict):
                self.append(DotDict(x))
            elif isinstance(x, (list, tuple)):
                self.append(DotList(x))
            else:
                self.append(x)
