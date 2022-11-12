import pytest
import psycopg
from src import config
from typing import List, Any
from psycopg import Connection
from typing import Callable
from src.dbmeta.connections.postgres import Postgres
from tests._fix_db_meta import TEST_DB_STRING
from psycopg.errors import OperationalError
from time import sleep

class DBConnection:
    conn: Connection | None = None

    def execute(self, sql: str, args: List[Any] = []) -> List[Any]:
            db = self.conn.cursor()
            db.execute(sql, args)
            self.conn.commit()

    def create_schema(self, names: List[str]) -> None:
        if self.conn is None:
            raise Exception("Connection is None")

        for schema in names:
            self.conn.execute(f"CREATE SCHEMA {schema}")
        self.conn.commit()

    def setup(self) -> None:
        temp_conn = psycopg.Connection.connect(TEST_DB_STRING + "/postgres")
        temp_conn.autocommit = True
        temp_conn.execute("DROP DATABASE IF EXISTS test")
        temp_conn.execute("CREATE DATABASE test")
        temp_conn.close()

        self.conn = psycopg.Connection.connect(TEST_DB_STRING + "/test")

    def close(self) -> None:
        self.conn.close()

@pytest.fixture
def db_connection():
    return DBConnection()

    
