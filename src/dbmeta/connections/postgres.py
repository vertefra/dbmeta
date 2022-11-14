from psycopg import Connection
from ..settings import config
from .database import IDatabase, Schema, Table, Column, UserDefined
from typing import List
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
        user_defined = self._query_custom_types()
        tables = self._query_tables(schema)
        columns = self._query_tables_columns(tables)

        m = Metadata()
        m.schema = schema
        m.tables = tables
        m.columns = columns
        m.user_defined = user_defined

        return m

    def _query_custom_types(self) -> List[UserDefined]:
        """Same query behind psql command `/dT+`"""
        sql = f"""
            SELECT 
                n.nspname as "schema",
                pg_catalog.format_type(t.oid, NULL) AS "name",
                t.typname AS "internal_name",
                CASE 
                    WHEN t.typrelid != 0
                        THEN CAST('tuple' AS pg_catalog.text)
                    WHEN t.typlen < 0
                        THEN CAST('var' AS pg_catalog.text)
                    ELSE CAST(t.typlen AS pg_catalog.text)
                END AS "size",
                pg_catalog.array_to_string(
                    ARRAY(
                        SELECT e.enumlabel
                        FROM pg_catalog.pg_enum e
                        WHERE e.enumtypid = t.oid
                        ORDER BY e.enumsortorder
                    ),
                    E'\n'
                ) AS "elements",
                pg_catalog.pg_get_userbyid(t.typowner) AS "owner",
                pg_catalog.array_to_string(t.typacl, E'\n') AS "access_privileges",
                pg_catalog.obj_description(t.oid, 'pg_type') as "description"
            FROM 
                pg_catalog.pg_type t
            LEFT JOIN 
                pg_catalog.pg_namespace n ON n.oid = t.typnamespace
            WHERE (
                    t.typrelid = 0 OR (
                        SELECT c.relkind = 'c' FROM pg_catalog.pg_class c WHERE c.oid = t.typrelid
                    )
                )
            AND NOT EXISTS (
                SELECT 1 FROM pg_catalog.pg_type el WHERE el.oid = t.typelem AND el.typarray = t.oid
            )
            AND n.nspname <> 'pg_catalog'
            AND n.nspname <> 'information_schema'
            AND pg_catalog.pg_type_is_visible(t.oid)
            ORDER BY 1, 2;
        """

        with self.__get_conn() as conn:
            db = conn.cursor()
            try:
                db.execute(sql)
                records = db.fetchall()

                return [UserDefined(record) for record in records]
            finally:
                db.close()

    def _query_tables_columns(self, tables: List[Table]) -> List[Column]:
        all_columns: List[Column] = []

        for table in tables:
            all_columns.extend(self._query_table_columns(table))

        return all_columns

    def _query_table_columns(self, table: Table) -> List[Column]:

        sql = """
            SELECT column_name, data_type, udt_name::regtype, *
            FROM information_schema.columns 
            WHERE table_schema = %s
            AND table_name=%s;
        """

        with self.__get_conn() as conn:
            db = conn.cursor()
            try:
                db.execute(sql, (table.table_schema, table.table_name))
                records = db.fetchall()

                columns = [Column(record) for record in records]

                table.columns = columns
                return columns
            finally:
                db.close()

    def _query_schema(self) -> List[Schema]:
        with self.__get_conn() as conn:
            db = conn.cursor()
            try:
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
            finally:
                db.close()

            return [Schema(record) for record in records]

    def _query_tables(self, schema: List[Schema]) -> List[Table]:

        all_tables: List[Table] = []

        with self.__get_conn() as conn:
            db = conn.cursor()
            try:

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
            finally:
                db.close()

        return all_tables

    def __get_conn(self) -> Connection:
        if config.database_url is None:
            raise Exception("No database_url found")

        return Connection.connect(config.database_url, row_factory=dict_row)
