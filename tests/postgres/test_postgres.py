from tests.postgres._fix_pg_connection import DBConnection, Postgres


def test_postgres_query_schema(db_connection: DBConnection, postgres: Postgres):
    cleanup = db_connection.create_schema(["schema_one", "schema_two"])

    schema = postgres._query_schema()

    assert len(schema) == 2
