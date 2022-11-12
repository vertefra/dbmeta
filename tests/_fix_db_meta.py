from src import dbmeta, config
import pytest


@pytest.fixture(autouse=True)
def test_config():
    config.database_url = "postgres://postgres:postgres@localhost:2345/test"
    return config

@pytest.fixture
def postgres_dbmeta():
    dbmeta.database = "postgres"
    return dbmeta
