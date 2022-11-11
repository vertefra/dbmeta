from .database import IDatabase, Column, Schema, Table
from .postgres import Postgres
from .exclude import exclude


def init(database_type: str) -> IDatabase:
    if database_type == "postgres":
        return Postgres()

    raise Exception(f"{database_type} not supported")
