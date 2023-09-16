"""SQLite helper utilities for writing Spotify data."""
from typing import Union

from db.sql import helper
from db.sql.helper import conn, cursor
from integrations.spotify.helper import flatten_spotify_episode, flatten_spotify_show
from integrations.spotify.models import SpotifyEpisode, SpotifyShow


def write_spotify_data_to_db(instance: Union[SpotifyShow, SpotifyEpisode]) -> None:
    table_name = instance.__table_name__
    instance_dict = (
        flatten_spotify_show(instance)
        if isinstance(instance, SpotifyShow)
        else flatten_spotify_episode(instance)
    )
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
