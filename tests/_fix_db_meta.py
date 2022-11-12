from src import dbmeta, config
import pytest

TEST_DB_STRING = "postgres://postgres:postgres@localhost:2345"


@pytest.fixture(autouse=True)
def test_config():
    config.database_url = TEST_DB_STRING + "/test"
    return config
