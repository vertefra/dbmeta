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