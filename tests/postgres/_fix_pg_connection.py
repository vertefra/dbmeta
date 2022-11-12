import pytest
import psycopg
from src import config
from typing import List
from psycopg import Connection
from typing import Callable
from src.dbmeta.connections.postgres import Postgres

class DBConnection:
    def __init__(self, c: Connection) -> None:
        self.conn = c

    def create_schema(self, schema_name: List[str]) -> Callable:
        def cleanup():
            for schema in schema_name:
                with self.conn.connect() as conn:
                    conn.transaction()

                    try:
                        conn.execute(f"DROP SCHEMA IF EXISTS {schema} ")
                        conn.commit()
                    finally:
                        conn.close()

        with self.conn.connect() as conn:
            conn.transaction()

            try:
                for schema in schema_name:
                    sql = f"CREATE SCHEMA IF NOT EXISTS {schema}"
                    conn.execute(sql)

                conn.commit()
                return cleanup
            finally:
                conn.close()


@pytest.fixture
def db_connection(test_config):
    c = psycopg.Connection.connect(test_config.database_url)
    return DBConnection(c)

@pytest.fixture
def postgres():
    return Postgres()
    