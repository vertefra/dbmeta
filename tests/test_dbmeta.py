def test_postgres_db_meta(postgres_dbmeta):
    assert postgres_dbmeta.database == "postgres"
