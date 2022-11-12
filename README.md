# dbmeta v0.0.10
## Database metadata extractor

Generate a Metadata object containing information about the database.

### Install
```bash
pip install dbmeta
```

### Use
```python
import dbmeta

db_type = 'postgres'
db_url = 'postgres://postgres:postgres@localhost:5432'
metadata = dbmeta.gen_metadata(db_type, db_url)
```

## Excluding schema or tables

Postgres system tables and schema are already excluded from the introspection.
To exclude other tables or schema use the `exclude` class

```python
from dbmeta import exclude

exclude.schema = ["hdb_catalog"]
exclude.tables = ["migrations"]

...
```

## Classes

### Metadata

```python
class Metadata:
    schema: List[Schema]
    tables: List[Table]
    columns: List[Column]

```


### Schema

```python
class Schema(DatabaseItem):
    catalog_name: str
    schema_name: str
    schema_owner: str
    tables: List[Table]
```
### Table

```python
class Table(DatabaseItem):
    table_catalog: str
    table_schema: str
    table_name: str
    table_type: str
    columns: List[Column]
```

### Column
```python
class Column(DatabaseItem):
    udt_name: str
    table_catalog: str
    table_schema: str
    table_name: str
    column_name: str
    ordinal_position: int
    column_default: str | None
    is_nullable: Literal["YES"] | Literal["NO"]
    data_type: str
    character_maximum_length: int | None
    is_updatable: bool

```


