"""SQLite helper utilities for writing YouTube data."""
from typing import Union

from db.sql import helper
from db.sql.helper import conn, cursor
from integrations.youtube.helper import flatten_video
from integrations.youtube.models import YoutubeChannel, YoutubeVideo


def write_youtube_data_to_db(instance: Union[YoutubeChannel, YoutubeVideo]) -> None:
    """Writes either the Channel or Video instance to their respective
    SQLite tables."""
    table_name = instance.__table_name__
    if isinstance(instance, YoutubeVideo):
        instance_dict = flatten_video(instance)
    else:
        instance_dict = instance.__dict__
    instance_dict.pop("__table_name__", None)

    if not helper.check_if_table_exists(cursor=cursor, table_name=table_name):
        helper.create_table(conn=conn, cursor=cursor, table_name=table_name)

    # only write to the SQLite DB if the primary key is unique
    row_insertion_is_valid = helper.single_row_insertion_is_valid(
        row_data=instance_dict, table_name=table_name
    )
    if row_insertion_is_valid:
        helper.write_to_database(
            conn=conn, cursor=cursor, table_name=table_name, data=instance_dict
        )
