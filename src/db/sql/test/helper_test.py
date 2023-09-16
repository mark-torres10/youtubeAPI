import os

import pytest

from db.sql.helper import (
    check_if_table_exists,
    create_table,
    test_conn,
    test_cursor,
    TEST_DB_NAME,
)


@pytest.fixture(scope="module", autouse=True)
def cleanup_database():
    yield

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


def test_create_table(cleanup_database):
    # Test creating a table
    create_table(conn=test_conn, cursor=test_cursor, table_name="youtube_channels")
    assert (
        check_if_table_exists(cursor=test_cursor, table_name="youtube_channels") is True
    )
