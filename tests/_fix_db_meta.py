from src import dbmeta, config
import pytest 

@pytest.fixture(autouse=True)
def postgres_dbmeta():
    config.database_url = "postgres://postgres:postgres@localhost:2345/test"
    dbmeta.database = 'postgres'
    return dbmeta
