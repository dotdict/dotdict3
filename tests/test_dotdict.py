from dotdict3 import DotDict, DotList
import pytest


class TestDotDict:
    def test_basic_initialization(self):
        d = DotDict({"a": 1, "b": 2})
        assert d["a"] == 1
        assert d["b"] == 2

    def test_dot_notation_access(self):
        d = DotDict({"name": "John", "age": 30})
        assert d.name == "John"
        assert d.age == 30

    def test_dot_notation_assignment(self):
        d = DotDict({})
        d.name = "Alice"
        assert d["name"] == "Alice"
        assert d.name == "Alice"

    def test_nested_dict_conversion(self):
        d = DotDict({"user": {"name": "Bob", "age": 25}})
        assert isinstance(d.user, DotDict)
        assert d.user.name == "Bob"
        assert d.user.age == 25

    def test_deeply_nested_dict(self):
        d = DotDict({"level1": {"level2": {"level3": {"value": 42}}}})
        assert isinstance(d.level1, DotDict)
        assert isinstance(d.level1.level2, DotDict)
        assert isinstance(d.level1.level2.level3, DotDict)
        assert d.level1.level2.level3.value == 42

    def test_list_conversion(self):
        d = DotDict({"data": [1, 2, 3]})
        assert isinstance(d.data, DotList)
        assert list(d.data) == [1, 2, 3]

    def test_mixed_nested_structures(self):
        d = DotDict(
            {"data": [{"name": "item1", "value": 10}, {"name": "item2", "value": 20}]}
        )
        assert isinstance(d.data, DotList)
        assert isinstance(d.data[0], DotDict)
        assert d.data[0].name == "item1"
        assert d.data[1].value == 20

    def test_prevent_double_conversion(self):
        inner_dict = DotDict({"a": 1})
        d = DotDict({"inner": inner_dict})
        assert d.inner is inner_dict

    def test_setitem_after_initialization(self):
        d = DotDict({"a": 1})
        d["nested"] = {"b": 2}
        assert isinstance(d.nested, DotDict)
        assert d.nested.b == 2

    def test_del_attribute(self):
        d = DotDict({"a": 1, "b": 2})
        del d.a
        assert "a" not in d
        assert d.b == 2

    def test_primitive_values(self):
        d = DotDict(
            {"string": "hello", "int": 42, "float": 3.14, "bool": True, "none": None}
        )
        assert d.string == "hello"
        assert d.int == 42
        assert d.float == 3.14
        assert d.bool is True
        assert d.none is None

    def test_dict_assignment(self):
        d = DotDict({})
        d.a = {"b": 2}
        assert d.a.b == 2

    def test_dict_assignment_with_list(self):
        d = DotDict({})
        d.a = [{"b": 2}]
        assert d.a[0].b == 2


class TestDotList:
    def test_basic_initialization(self):
        l = DotList([1, 2, 3])
        assert list(l) == [1, 2, 3]

    def test_dict_conversion_in_list(self):
        l = DotList([{"a": 1}, {"b": 2}])
        assert isinstance(l[0], DotDict)
        assert isinstance(l[1], DotDict)
        assert l[0].a == 1
        assert l[1].b == 2

    def test_nested_list_conversion(self):
        l = DotList([[1, 2], [3, 4]])
        assert isinstance(l[0], DotList)
        assert isinstance(l[1], DotList)
        assert list(l[0]) == [1, 2]
        assert list(l[1]) == [3, 4]

    def test_deeply_nested_structures(self):
        l = DotList([{"name": "item", "values": [1, 2, 3], "nested": {"key": "value"}}])
        assert isinstance(l[0], DotDict)
        assert isinstance(l[0]["values"], DotList)
        assert isinstance(l[0]["nested"], DotDict)
        assert l[0]["nested"]["key"] == "value"

    def test_append_dict(self):
        l = DotList([])
        l.append({"a": 1})
        assert isinstance(l[0], DotDict)
        assert l[0].a == 1

    def test_append_list(self):
        l = DotList([])
        l.append([1, 2, 3])
        assert isinstance(l[0], DotList)
        assert list(l[0]) == [1, 2, 3]

    def test_append_primitive(self):
        l = DotList([])
        l.append(42)
        l.append("hello")
        l.append(None)
        assert l[0] == 42
        assert l[1] == "hello"
        assert l[2] is None

    def test_prevent_double_conversion(self):
        inner_dict = DotDict({"a": 1})
        l = DotList([inner_dict])
        assert l[0] is inner_dict

    def test_prevent_double_list_conversion(self):
        inner_list = DotList([1, 2, 3])
        l = DotList([inner_list])
        assert l[0] is inner_list

    def test_mixed_types(self):
        l = DotList([1, "string", {"key": "value"}, [1, 2], None, True])
        assert l[0] == 1
        assert l[1] == "string"
        assert isinstance(l[2], DotDict)
        assert isinstance(l[3], DotList)
        assert l[4] is None
        assert l[5] is True

    def test_list_insert(self):
        l = DotList([{'a': 1}])
        l.insert(0, {'b': 2})
        assert l[0].b == 2

class TestIntegration:
    def test_complex_nested_structure(self):
        data = {
            "users": [
                {
                    "name": "Alice",
                    "scores": [95, 87, 92],
                    "metadata": {"joined": "2024-01-01", "tags": ["admin", "active"]},
                },
                {
                    "name": "Bob",
                    "scores": [88, 90, 85],
                    "metadata": {"joined": "2024-02-15", "tags": ["user"]},
                },
            ],
            "settings": {"theme": "dark", "notifications": True},
        }

        d = DotDict(data)

        assert d.users[0].name == "Alice"
        assert d.users[0].scores[1] == 87
        assert d.users[0].metadata.tags[0] == "admin"
        assert d.users[1].name == "Bob"
        assert d.settings.theme == "dark"

    def test_modification_after_creation(self):
        d = DotDict({"a": 1})
        d["b"] = {"c": {"d": 2}}
        assert isinstance(d["b"], DotDict)
        assert isinstance(d["b"]["c"], DotDict)
        assert d["b"]["c"]["d"] == 2

    def test_list_append_after_creation(self):
        d = DotDict({"data": []})
        d["data"].append({"name": "new"})
        assert isinstance(d["data"][0], DotDict)
        assert d.data[0].name == "new"


class TestEdgeCases:
    def test_empty_dict(self):
        d = DotDict({})
        assert len(d) == 0

    def test_empty_dict_error(self):
        with pytest.raises(TypeError):
            DotDict()

    def test_empty_list(self):
        l = DotList([])
        assert len(l) == 0

    def test_empty_list_error(self):
        with pytest.raises(TypeError):
            DotList()

    def test_attribute_error_on_missing_key(self):
        d = DotDict({"a": 1})
        with pytest.raises(KeyError):
            _ = d.missing_key

    def test_dict_methods_still_work(self):
        d = DotDict({"a": 1, "b": 2})
        assert d.keys()
        assert d.values()
        assert d.items()
        assert "a" in d

    def test_list_methods_still_work(self):
        l = DotList([1, 2, 3])
        assert len(l) == 3
        l.extend([4, 5])
        assert len(l) == 5
        assert l.pop() == 5

    @pytest.mark.parametrize("arg", [int, list, set, str, tuple])
    def test_invalid_input(self, arg):
        with pytest.raises(AttributeError):
            DotDict(arg())
