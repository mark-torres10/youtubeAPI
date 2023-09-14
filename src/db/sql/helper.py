import sqlite3
from typing import Dict

import pandas as pd

from db.sql.schemas import TABLE_NAME_TO_SCHEMA_MAP

SQLITE_DB_NAME = "data.db"
TEST_DB_NAME = "test-data.db"

conn = sqlite3.connect(SQLITE_DB_NAME)
cursor = conn.cursor()

def generate_create_table_statement(table_name: str) -> str:
    schema = TABLE_NAME_TO_SCHEMA_MAP[table_name]
    return f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {schema}
        )
    """


def create_table(
    conn: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    table_name: str
) -> None:
    create_table_statement = generate_create_table_statement(table_name)
    cursor.execute(create_table_statement)
    conn.commit()


def check_if_table_exists(
    cursor: sqlite3.Cursor,
    table_name: str
) -> bool:
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    cursor.execute(query, (table_name,))
    result = cursor.fetchone()
    return result is not None


def write_to_database(
    conn: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    table_name: str,
    data: Dict
) -> None:
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    values = tuple(data.values())
    insert_query = (
        f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    )
    cursor.execute(insert_query, values)
    conn.commit()


def get_all_table_results_as_df(table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    return df
