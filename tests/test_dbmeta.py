from src import exclude
from src.dbmeta.connections import Postgres
from src import dbmeta


def test_exclude(db_connection):
    db_connection.setup()
    db_connection.create_schema(["exclude_this"])
    exclude.schema = ["exclude_this"]
    metadata = dbmeta.gen_metadata("postgres")

    assert len(metadata.schema) == 1

    db_connection.close()
