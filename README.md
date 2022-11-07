# dbmeta
## Database metadata extractor

Use

```
import dbmeta

db_type = 'postgres'
db_url = ''
metadata = dbmeta.gen_metadata(db_type, db_url)
```