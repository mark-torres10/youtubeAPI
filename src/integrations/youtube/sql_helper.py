"""SQL helper utilities specific to Youtube integration."""
from db.sql_helper import (
    close_connection, create_connection, execute_insert, execute_query
)


def create_tables():
    """Create necessary tables if they don't exist."""
    conn = create_connection()
    if conn:
        create_videos_table_query = """
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                published_at DATETIME,
                views INTEGER,
                likes INTEGER,
                dislikes INTEGER,
                comments INTEGER
            );
        """
        create_channels_table_query = """
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_handle TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                statistics_per_latest_videos TEXT
            );
        """
        execute_query(conn, create_videos_table_query)
        execute_query(conn, create_channels_table_query)
        close_connection(conn)
        print("SQLite tables created")

def insert_video(video_data):
    """Insert video data into the 'videos' table."""
    conn = create_connection()
    if conn:
        insert_video_query = """
            INSERT INTO videos (video_id, title, description, published_at, views, likes, dislikes, comments)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        execute_insert(conn, insert_video_query, video_data)
        close_connection(conn)

def insert_channel(channel_data):
    """Insert channel data into the 'channels' table."""
    conn = create_connection()
    if conn:
        insert_channel_query = """
            INSERT INTO channels (channel_handle, channel_id, statistics_per_latest_videos)
            VALUES (?, ?, ?);
        """
        execute_insert(conn, insert_channel_query, channel_data)
        close_connection(conn)
