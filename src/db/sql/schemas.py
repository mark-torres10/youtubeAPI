import sqlite3

TABLE_NAME_TO_SCHEMA_MAP = {
    "channels": """
        channel_id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        channel_title TEXT,
        publish_time TEXT,
        published_at TEXT,
        synctimestamp TEXT
    """,
    "videos": """
        video_id TEXT PRIMARY KEY,
        video_title TEXT,
        channel_id TEXT,
        channel_title TEXT,
        category_id TEXT,
        default_audio_language TEXT,
        default_language TEXT,
        description TEXT,
        live_broadcast_content TEXT,
        published_at TEXT,
        tags TEXT,
        view_count INTEGER,
        like_count INTEGER,
        favorite_count INTEGER,
        comment_count INTEGER,
        synctimestamp TEXT
    """
}

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