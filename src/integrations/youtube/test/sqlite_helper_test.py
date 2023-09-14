from integrations.youtube.models import Channel, Video

from db.sql.helper import conn, create_table, cursor, TEST_DB_NAME
from db.sql.test.helper_test import cleanup_database
from integrations.youtube.sqlite_helper import (
    get_all_table_results_as_df, write_youtube_data_to_db
)
from integrations.youtube.test import test_data

def test_write_to_database_channel(cleanup_database):
    # Test writing a Channel instance to the database
    create_table(conn=conn, cursor=cursor, table_name="channels")
    channel = Channel(**test_data.MOCK_CHANNEL_METADATA)

    write_youtube_data_to_db(instance=channel)

    # Check if the data was written successfully
    query = "SELECT * FROM channels WHERE channel_id='test_channel_id'"
    cursor.execute(query)
    result = cursor.fetchone()
    assert result is not None


def test_get_all_table_results_as_df_with_channel():
    df = get_all_table_results_as_df("channels")

    # Assert the length of the DataFrame
    assert len(df) == 1

    # Assert the content of the DataFrame
    for field, value in test_data.MOCK_CHANNEL_METADATA.items():
        assert df[field][0] == value


def test_write_to_database_video(cleanup_database):
    # Test writing a Video instance to the database
    create_table(conn=conn, cursor=cursor, table_name="videos")
    video = Video(
        video_id="test_video_id",
        metadata={
            "video_id": "test_video_id",
            "video_title": "Test Video",
            "channel_id": "test_channel_id",
            "channel_title": "Test Channel",
            "category_id": "123",
            "default_audio_language": "en",
            "default_language": "en",
            "description": "Test video description",
            "live_broadcast_content": "none",
            "published_at": "2023-09-10T00:00:00Z",
            "tags": ','.join(["tag1", "tag2"]),
        },
        statistics={
            "view_count": 100,
            "like_count": 50,
            "favorite_count": 10,
            "comment_count": 5,
        },
        synctimestamp="2023-09-10T00:00:00Z",
    )

    write_youtube_data_to_db(instance=video)

    query = "SELECT * FROM videos WHERE video_id='test_video_id'"
    cursor.execute(query)
    result = cursor.fetchone()
    assert result is not None
