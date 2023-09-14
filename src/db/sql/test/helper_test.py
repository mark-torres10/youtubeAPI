import os

import pytest

from db.sql.helper import (
    check_if_table_exists, conn, create_table, cursor, TEST_DB_NAME
)

@pytest.fixture(scope="module", autouse=True)
def cleanup_database():
    yield

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


def test_create_table(cleanup_database):
    # Test creating a table
    create_table(conn=conn, cursor=cursor, table_name="channels")
    assert check_if_table_exists(cursor=cursor, table_name="channels") is True
