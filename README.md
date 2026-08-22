# BitDB

Lightweight JSON database for Python.

BitDB is a simple embedded database designed for small Python projects that need persistent data storage without setting up a full database server.

## Features

* Simple Python API
* JSON-based storage
* Collections
* Insert, search, update and delete operations
* Automatic document IDs
* Unique fields for preventing duplicates
* Custom exceptions
* Collection management
* Lightweight and easy to integrate
* Built-in test suite

## Installation

### From source

Clone the repository:

```bash
git clone https://github.com/bitlineofficial/BitDB.git
cd BitDB
```

Install the package:

```bash
pip install .
```

### Development installation

For development, install the project in editable mode:

```bash
pip install -e .
```

Install the test framework:

```bash
pip install pytest
```

## Quick Start

Create a database:

```python
from bitdb import Database

db = Database("database.json")
```

Create a collection:

```python
users = db.collection("users")
```

Insert a document:

```python
user_id = users.insert_one({
    "name": "Mineri",
    "age": 16,
    "balance": 100
})

print(user_id)
```

A generated document ID will look similar to:

```text
jx_a83f91c42d7e
```

The database file will contain:

```json
{
    "users": [
        {
            "_id": "jx_a83f91c42d7e",
            "name": "Mineri",
            "age": 16,
            "balance": 100
        }
    ]
}
```

## Collections

A collection is a group of related documents.

Create or access a collection:

```python
users = db.collection("users")
```

Create multiple collections:

```python
users = db.collection("users")
products = db.collection("products")
payments = db.collection("payments")
```

Get all collection names:

```python
print(db.collections())
```

Example output:

```text
['users', 'products', 'payments']
```

Delete an entire collection:

```python
db.delete_collection("payments")
```

## Documents

BitDB stores documents as Python dictionaries.

Example:

```python
{
    "name": "Mineri",
    "age": 16,
    "balance": 100
}
```

When inserted, BitDB automatically adds an `_id` field:

```python
{
    "_id": "jx_a83f91c42d7e",
    "name": "Mineri",
    "age": 16,
    "balance": 100
}
```

## Insert Documents

### Insert one document

```python
users.insert_one({
    "name": "Mineri",
    "age": 16,
    "balance": 100
})
```

`insert_one()` returns the generated document ID.

```python
user_id = users.insert_one({
    "name": "Alex",
    "age": 17
})

print(user_id)
```

### Insert multiple documents

```python
users.insert_many([
    {
        "name": "Mineri",
        "age": 16
    },
    {
        "name": "Alex",
        "age": 17
    },
    {
        "name": "John",
        "age": 18
    }
])
```

## Preventing Duplicate Documents

Collections can define unique fields.

For example, to make `name` unique:

```python
users = db.collection(
    "users",
    unique_fields=["name"]
)
```

Now BitDB will prevent duplicate names.

```python
users.insert_one({
    "name": "Mineri",
    "age": 16
})
```

Trying to insert another document with the same name will raise:

```python
DuplicateDocumentError
```

Example:

```python
from bitdb import Database
from bitdb.exceptions import DuplicateDocumentError

db = Database("database.json")

users = db.collection(
    "users",
    unique_fields=["name"]
)

try:
    users.insert_one({
        "name": "Mineri",
        "age": 17
    })
except DuplicateDocumentError as error:
    print(error)
```

## Find Documents

### Find one document

```python
user = users.find_one(name="Mineri")

print(user)
```

Example result:

```python
{
    "_id": "jx_a83f91c42d7e",
    "name": "Mineri",
    "age": 16,
    "balance": 100
}
```

If no matching document exists, `find_one()` returns `None`.

```python
user = users.find_one(name="Unknown")

if user is None:
    print("User not found.")
```

### Find multiple documents

```python
users = db.collection("users")

users.insert_one({
    "name": "Mineri",
    "age": 16
})

users.insert_one({
    "name": "Alex",
    "age": 16
})

users.insert_one({
    "name": "John",
    "age": 18
})

result = users.find(age=16)

print(result)
```

Example:

```python
[
    {
        "_id": "jx_a83f91c42d7e",
        "name": "Mineri",
        "age": 16
    },
    {
        "_id": "jx_72bd18e4fa91",
        "name": "Alex",
        "age": 16
    }
]
```

## Update Documents

Update one document by a field and value:

```python
users.update_one(
    "name",
    "Mineri",
    {
        "balance": 500
    }
)
```

The document changes from:

```python
{
    "name": "Mineri",
    "age": 16,
    "balance": 100
}
```

to:

```python
{
    "name": "Mineri",
    "age": 16,
    "balance": 500
}
```

`update_one()` returns:

```python
True
```

when a matching document was updated.

If no matching document exists:

```python
False
```

## Delete Documents

Delete one document:

```python
users.delete_one(
    "name",
    "Alex"
)
```

If the document is found, it is removed from the collection and the database is saved automatically.

The method returns:

```python
True
```

when a document was deleted and:

```python
False
```

when no matching document was found.

## Count Documents

Get the number of documents in a collection:

```python
count = users.count()

print(count)
```

Example:

```text
3
```

## Clear a Collection

Remove every document from a collection:

```python
users.clear()
```

After clearing:

```python
print(users.count())
```

Output:

```text
0
```

The collection itself still exists; only its documents are removed.

## Get Raw Collection Data

You can access the documents currently stored in a collection:

```python
data = users.get_data()

print(data)
```

Example:

```python
[
    {
        "_id": "jx_a83f91c42d7e",
        "name": "Mineri",
        "age": 16
    }
]
```

## Complete Example

```python
from bitdb import Database
from bitdb.exceptions import DuplicateDocumentError


db = Database("database.json")

users = db.collection(
    "users",
    unique_fields=["name"]
)


# Insert users
try:
    users.insert_one({
        "name": "Mineri",
        "age": 16,
        "balance": 100
    })

    users.insert_one({
        "name": "Alex",
        "age": 17,
        "balance": 250
    })

except DuplicateDocumentError as error:
    print(error)


# Find one user
user = users.find_one(name="Mineri")

print("Found:")
print(user)


# Find multiple users
users_with_age_16 = users.find(age=16)

print("Users with age 16:")
print(users_with_age_16)


# Update a user
users.update_one(
    "name",
    "Mineri",
    {
        "balance": 500
    }
)


# Count users
print("User count:", users.count())


# Delete a user
users.delete_one(
    "name",
    "Alex"
)


# Show all collections
print("Collections:", db.collections())
```

## Exceptions

BitDB provides custom exceptions for common errors.

### Base exception

```python
from bitdb.exceptions import JexDBError
```

`JexDBError` is the base exception for BitDB-specific errors.

### DuplicateDocumentError

Raised when a document violates a unique field:

```python
from bitdb.exceptions import DuplicateDocumentError
```

### InvalidDocumentError

Raised when an invalid document is passed to an operation:

```python
from bitdb.exceptions import InvalidDocumentError
```

### CollectionNotFoundError

Used for operations that require a collection that does not exist:

```python
from bitdb.exceptions import CollectionNotFoundError
```

### DocumentNotFoundError

Used when an operation requires a document that cannot be found:

```python
from bitdb.exceptions import DocumentNotFoundError
```

## Testing

BitDB uses `pytest`.

Install it:

```bash
pip install pytest
```

Run the full test suite:

```bash
python -m pytest
```

Example:

```text
============================= test session starts =============================
collected 11 items

tests/test_collection.py .......
tests/test_database.py ....

============================== 11 passed ==============================
```

## Project Structure

```text
BitDB/
│
├── bitdb/
│   ├── __init__.py
│   ├── database.py
│   ├── collection.py
│   ├── document.py
│   └── exceptions.py
│
├── tests/
│   ├── test_collection.py
│   └── test_database.py
│
├── README.md
├── LICENSE
├── pyproject.toml
└── .gitignore
```

## Design Goals

BitDB is intentionally simple.

It is designed for projects where a lightweight local JSON database is enough and running a separate database server would be unnecessary.

BitDB is a good fit for:

* Telegram bots
* Small desktop applications
* Prototypes
* Personal projects
* Local tools
* Educational projects
* Small APIs

BitDB is not intended to replace production database systems such as PostgreSQL, MySQL, or MongoDB for large-scale applications.

## Roadmap

Planned improvements include:

* More powerful query operators
* Better filtering
* Search by document ID
* Improved validation
* More database exceptions
* More extensive tests
* Performance improvements
* Better documentation
* Package publication on PyPI
* Stable release versions

## Contributing

Contributions, bug reports and suggestions are welcome.

Before submitting changes, run:

```bash
python -m pytest
```

Please make sure all tests pass before opening a pull request.

## License

BitDB is distributed under the MIT License.

See the `LICENSE` file for the full license text.

## Author

Developed by **BitLine**.

GitHub:

https://github.com/bitlineofficial/BitDB

---

**BitDB — simple JSON storage for Python projects.**
