"""SQLite helper utilities for writing YouTube data."""
import sqlite3
from typing import Union

import pandas as pd

from integrations.youtube import helper
from integrations.youtube.models import Channel, Video

conn = sqlite3.connect('youtube_data.db')
cursor = conn.cursor()


TABLE_TO_CREATE_TABLE_STATEMENT = {
    "channels": """
        CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            channel_title TEXT,
            publish_time TEXT,
            published_at TEXT,
            synctimestamp TEXT
        )
    """,
    "videos": """
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            video_title TEXT
            channel_id TEXT
            channel_title TEXT
            category_id TEXT
            default_audio_language TEXT
            default_language TEXT
            description TEXT
            live_broadcast_content TEXT
            published_at TEXT
            tags TEXT
            view_count INTEGER
            like_count INTEGER
            favorite_count INTEGER
            comment_count INTEGER
            synctimestamp TEXT
        )
    """
}


def create_table(table_name: str) -> None:
    create_table_statement = TABLE_TO_CREATE_TABLE_STATEMENT[table_name]
    cursor.execute(create_table_statement)
    conn.commit()


def check_if_table_exists(table_name: str) -> None:
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    cursor.execute(query, (table_name,))
    result = cursor.fetchone()
    return result is not None


def write_to_database(instance: Union[Channel, Video]) -> None:
    """Writes either the Channel or Video instance to their respective
    SQLite tables."""
    table_name = instance.__table_name__
    if isinstance(instance, Video):
        instance_dict = helper.flatten_video(Video)
    else:
        instance_dict = instance.__dict__
    instance_dict.pop('__table_name__', None)

    if not check_if_table_exists(table_name):
        create_table(table_name)

    columns = ', '.join(instance_dict.keys())
    placeholders = ', '.join(['?'] * len(instance_dict))
    values = tuple(instance_dict.values())

    insert_query = (
        f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    )
    cursor.execute(insert_query, values)
    conn.commit()


def get_all_table_results_as_df(table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    return df
