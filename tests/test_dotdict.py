from dotdict3 import DotDict, DotList
import pytest


def test_empty():
    dotdict = DotDict()
    assert dotdict == {}

def test_one_layer():
    dotdict = DotDict({"a": "b"})
    assert dotdict.a == "b"

def test_two_layers():
    dotdict = DotDict({"a": {"b": "c"}})
    assert dotdict.a.b == "c"

def test_list_in_dict():
    dotdict = DotDict({"a": [{"b": "c"}]})
    assert dotdict.a[0].b == "c"

def test_list():
    dotlist = DotList([{"a": "b"}])
    assert dotlist[0].a == "b"

def test_tuple_in_dict():
    dotdict = DotDict({"a": ({"b": "c"},)})
    assert dotdict.a[0].b == "c"

def test_tuple():
    dotlist = DotList(({"a": "b"},))
    assert dotlist[0].a == "b"

def test_value_as_int():
    dotdict = DotDict({"a": 2})
    assert dotdict.a == 2

@pytest.mark.parametrize("arg", [
    int,
    list,
    set,
    str,
    tuple,
])
def test_invalid_input(arg):
    with pytest.raises(AttributeError):
        DotDict(arg())
