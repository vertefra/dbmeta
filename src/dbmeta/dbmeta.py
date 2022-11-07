from .connections import init
from .connections.database import Metadata
from .settings import config

_supported_databases = ["postgres"]

class dbmeta:
    database: str

    @classmethod
    def gen_metadata(
        cls, database: str | None = None, database_url: str | None = None
    ) -> Metadata:

        if database:
            cls.database = database

        if database_url:
            config.database_url = database_url

        if cls.database is None:
            raise Exception(
                f"Please, provide a valid database type. Supported databases: {','.join(_supported_databases)}"
            )

        if cls.database not in _supported_databases:
            raise Exception(
                f"Database {cls.database} is not supported. Supported databases: {','.join(_supported_databases)}"
            )

        if config.database_url is None:
            raise Exception(f"I need a database url to inspect")

        db = init(cls.database)
        return db.inspect_database()
