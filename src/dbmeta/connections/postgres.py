from psycopg import Connection
from ..settings import config
from .database import IDatabase, Schema, Table, Column
from typing import Any, List
from psycopg.rows import dict_row
from .exclude import exclude
from .database import Metadata


class Postgres(IDatabase):
    exclude_schema: List[str] = ["pg_toast", "pg_catalog", "information_schema"]
    exclude_tables: List[str] = []

    def __init__(self) -> None:
        self.exclude_schema.extend(exclude.schema)
        self.exclude_tables.extend(exclude.tables)

    def inspect_database(self) -> Metadata:
        schema = self._query_schema()
        tables = self._query_tables(schema)
        columns = self._query_tables_columns(tables)
        return Metadata(schema, tables, columns)

    def _query_tables_columns(self, tables: List[Table]) -> List[Column]:
        all_columns: List[Column] = []

        for table in tables:
            all_columns.extend(self._query_table_columns(table))

        return all_columns

    def _query_table_columns(self, table: Table) -> List[Column]:

        sql = """
            SELECT column_name, data_type, udt_name::regtype, *
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            AND table_name=%s;
        """

        with self.__get_conn() as conn:
            db = conn.cursor()

            db.execute(sql, (table.table_name,))
            records = db.fetchall()

            columns = [Column(record) for record in records]

            table.columns = columns
            return columns

    def _query_schema(self) -> List[Schema]:
        with self.__get_conn() as conn:
            db = conn.cursor()

            db.execute(
                f""" 
                SELECT 
                    * 
                FROM 
                    information_schema.schemata 
                WHERE
                    schema_name != ALL(%s) 

            """,
                (self.exclude_schema,),
            )

            records = db.fetchall()

            return [Schema(record) for record in records]

    def _query_tables(self, schema: List[Schema]) -> List[Table]:

        all_tables: List[Table] = []

        with self.__get_conn() as conn:
            db = conn.cursor()

            for _schema in schema:
                db.execute(
                    f"""
                    SELECT 
                        table_catalog,
                        table_schema,
                        table_name,
                        table_type
                    FROM 
                        information_schema.tables
                    WHERE
                        table_schema = %s
                    AND
                        table_name != ALL( %s )
                """,
                    (_schema.schema_name, self.exclude_tables),
                )

                records = db.fetchall()

                tables = [Table(record) for record in records]

                _schema.tables = tables

                all_tables.extend(tables)

        return all_tables

    def __get_conn(self) -> Connection:
        return Connection.connect(config.database_url, row_factory=dict_row)
