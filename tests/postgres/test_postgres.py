from tests.postgres._fix_pg_connection import DBConnection, Postgres
from tests.postgres.tables import set_one
import pytest


def test_postgres_query_schema(db_connection: DBConnection):
    db_connection.setup()
    schema_list = ["schema_one", "schema_two"]
    postgres = Postgres()
    db_connection.create_schema(schema_list)
    schema = postgres._query_schema()

    schema_list.append("public")
    assert len(schema) == len(schema_list)

    for _schema in schema:
        assert _schema.schema_name in schema_list
        assert _schema.catalog_name == "test"
        assert _schema.schema_owner is not None
        assert _schema.tables is not None

    db_connection.close()


@pytest.mark.parametrize("tables", [set_one])
def test_postgres_query_tables(db_connection: DBConnection, tables):
    db_connection.setup()
    postgres = Postgres()

    for table_name, columns in tables.items():
        sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {", ".join(columns)}
            )
        """
        db_connection.execute(sql)

    schema = postgres._query_schema()
    tables = postgres._query_tables(schema)

    assert len(schema) == 1
    assert len(schema[0].tables) == 2
    assert schema[0].schema_name == "public"

    schema_tables = []
    schema_names = [s.schema_name for s in schema]
    for s in schema:
        schema_tables.extend([t.table_name for t in s.tables])

    assert len(tables) == 2

    for table in tables:
        assert table.table_name in schema_tables
        assert table.table_name in [t.table_name for t in tables]
        assert table.table_catalog == "test"
        assert table.table_schema in schema_names
        assert table.columns is not None

    db_connection.close()
