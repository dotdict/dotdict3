# dotdict3

A lightweight Python package for accessing dictionary keys and list elements using dot notation with automatic recursive conversion of nested structures.

## Installation

```bash
pip install dotdict3
```

```
>>> from dotdict3 import DotDict
>>> d = DotDict({"a": "b"})
>>> d.a
'b'
```

## Features

- **Dot notation access**: Access dictionary keys as attributes (`data.key` instead of `data['key']`)
- **Automatic conversion**: Nested dictionaries and iterables are automatically converted to `DotDict` and `DotList`
- **Recursive processing**: Works seamlessly with deeply nested structures
- **Standard compatibility**: Fully compatible with built-in `dict` and `list` operations

## Quick Start

```python
from dotdict3 import DotDict

data = DotDict({
    'name': 'John',
    'age': 30,
    'address': {
        'city': 'New York',
        'zipcode': '10001'
    }
})

# Access with dot notation
print(data.name)              # 'John'
print(data.address.city)      # 'New York'

# Still works with bracket notation
print(data['age'])            # 30
```

## Classes

### DotDict

A dictionary subclass that allows attribute-style access to keys.

#### Features

- **Attribute access**: Get, set, and delete keys using dot notation
- **Automatic nesting**: Nested dictionaries are automatically converted to `DotDict`
- **Iterable conversion**: Lists, tuples, sets, and ranges are converted to `DotList`
- **Dict compatibility**: All standard `dict` methods work as expected

#### Usage

```python
from dotdict3 import DotDict

# Basic usage
user = DotDict({'name': 'Alice', 'role': 'admin'})
print(user.name)  # 'Alice'

# Setting values
user.email = 'alice@example.com'
print(user.email)  # 'alice@example.com'

# Nested dictionaries
config = DotDict({
    'database': {
        'host': 'localhost',
        'port': 5432
    }
})
print(config.database.host)  # 'localhost'

# Deleting keys
del user.role
```

### DotList

A list subclass that automatically converts nested dictionaries and iterables.

#### Features

- **Automatic conversion**: Dictionaries in the list become `DotDict` instances
- **Nested iterables**: Lists, tuples, sets, and ranges become `DotList` instances
- **List compatibility**: All standard `list` methods work as expected

#### Usage

```python
from dotdict3 import DotList

# Basic usage
items = DotList([1, 2, 3])
print(items[0])  # 1

# Lists with dictionaries
users = DotList([
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25}
])
print(users[0].name)  # 'Alice'

# Nested lists
matrix = DotList([[1, 2], [3, 4]])
print(matrix[0][1])  # 2

# Appending
users.append({'name': 'Charlie', 'age': 35})
print(users[2].name)  # 'Charlie'
```

## Advanced Usage

### Complex Nested Structures

```python
from dotdict3 import DotDict

data = DotDict({
    'users': [
        {
            'name': 'Alice',
            'scores': [95, 87, 92],
            'metadata': {
                'joined': '2024-01-01',
                'tags': ['admin', 'active']
            }
        },
        {
            'name': 'Bob',
            'scores': [88, 90, 85],
            'metadata': {
                'joined': '2024-02-15',
                'tags': ['user']
            }
        }
    ],
    'settings': {
        'theme': 'dark',
        'notifications': True
    }
})

# Access deeply nested data
print(data.users[0].name)                    # 'Alice'
print(data.users[0].scores[1])               # 87
print(data.users[0].metadata.tags[0])        # 'admin'
print(data.settings.theme)                   # 'dark'
```

### Working with JSON

Perfect for working with JSON data:

```python
import json
from dotdict3 import DotDict

# Load JSON
with open('config.json') as f:
    config = DotDict(json.load(f))

# Access nested configuration
db_host = config.database.host
api_key = config.api.credentials.key
```

### Dynamic Updates

```python
from dotdict3 import DotDict

data = DotDict({})

# Add nested structure dynamically
data['user'] = {
    'profile': {
        'name': 'Alice',
        'preferences': ['email', 'sms']
    }
}

# Automatically converted
print(data.user.profile.name)                # 'Alice'
print(data.user.profile.preferences[0])      # 'email'
```

## Important Notes

### Reserved Names

Be careful with dictionary method names. Since `DotDict` inherits from `dict`, built-in method names will shadow your keys:

```python
data = DotDict({'items': [1, 2, 3]})

# This returns the dict.items() method, not your data!
print(data.items)  # <built-in method items>

# Use bracket notation instead
print(data['items'])  # DotList([1, 2, 3])
```

Common reserved names to avoid:
- `clear`
- `copy`
- `get`
- `items`
- `keys`
- `pop`
- `setdefault`
- `update`
- `values`

### Type Checking

The classes include automatic type checking to prevent double conversion:

```python
from dotdict3 import DotDict

inner = DotDict({'a': 1})
outer = DotDict({'inner': inner})

# inner is not converted again
assert outer['inner'] is inner  # True
```

### Iterable Conversion

All iterables (except strings and bytes) are converted to `DotList`:

```python
data = DotDict({
    'list': [1, 2, 3],
    'tuple': (4, 5, 6),
    'set': {7, 8, 9},
    'range': range(10, 13)
})

# All become DotList
assert isinstance(data['list'], DotList)   # True
assert isinstance(data['tuple'], DotList)  # True
assert isinstance(data['set'], DotList)    # True
assert isinstance(data['range'], DotList)  # True
```

## Compatibility

- Python 3.6+
- Compatible with all standard `dict` and `list` operations

## Use Cases

- **Configuration management**: Easy access to nested config files
- **API responses**: Simplify working with JSON API responses
- **Data processing**: Cleaner code when working with nested data structures
- **Settings objects**: Create intuitive settings/options objects

## Limitations

- String keys only (dictionary keys must be valid Python identifiers for dot notation)
- Watch out for reserved dictionary/list method names
- Dot notation won't work for keys with spaces or special characters

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Examples

### Example 1: Configuration File

```python
from dotdict3 import DotDict
import yaml

with open('config.yaml') as f:
    config = DotDict(yaml.safe_load(f))

# Easy access to nested config
database_url = f"{config.database.host}:{config.database.port}"
log_level = config.logging.level
```

### Example 2: API Response

```python
from dotdict3 import DotDict
import requests

response = requests.get('https://api.example.com/users/1')
user = DotDict(response.json())

print(f"{user.name} - {user.email}")
print(f"City: {user.address.city}")
```

### Example 3: Test Data

```python
from dotdict3 import DotDict

test_data = DotDict({
    'scenarios': [
        {'name': 'happy_path', 'expected': 200},
        {'name': 'not_found', 'expected': 404},
        {'name': 'server_error', 'expected': 500}
    ]
})

for scenario in test_data.scenarios:
    assert response.status_code == scenario.expected
```
