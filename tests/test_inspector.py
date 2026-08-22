import pytest
import sqlite3
import os
from app.inspector import DBDataInspector


@pytest.fixture
def temp_db(tmp_path):
    """Создает временную БД в файле для тестирования."""
    db_file = tmp_path / "test.db"
    db_uri = f"sqlite:///{db_file}"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test_table (id INT, val TEXT);")
    cursor.execute("INSERT INTO test_table VALUES (1, 'ok'), (2, NULL);")
    conn.commit()
    conn.close()

    return db_uri


def test_connection(temp_db):
    inspector = DBDataInspector(temp_db)
    assert inspector.check_connection() is True


def test_null_detection(temp_db):
    inspector = DBDataInspector(temp_db)
    overview = inspector.get_tables_overview()

    assert len(overview) == 1
    table = overview[0]
    assert table['table_name'] == 'test_table'
    assert table['total_rows'] == 2
    assert table['total_nulls'] == 1
    assert table['completeness_pct'] == 75.0