"""SQLite helper utilities for writing Spotify data."""
from typing import Union

from db.sql.helper import (
    conn, cursor, check_if_table_exists, create_table, write_to_database
)
from integrations.spotify import helper
from integrations.spotify.models import SpotifyEpisode, SpotifyShow

def write_spotify_data_to_db(
    instance: Union[SpotifyShow, SpotifyEpisode]
) -> None:
    table_name = instance.__table_name__
    instance_dict = (
        helper.flatten_spotify_show(instance)
        if isinstance(instance, SpotifyShow)
        else helper.flatten_spotify_episode(instance)
    )
    instance_dict.pop('__table_name__', None)
    if not check_if_table_exists(cursor=cursor, table_name=table_name):
        create_table(conn=conn, cursor=cursor, table_name=table_name)
    write_to_database(
        conn=conn, cursor=cursor, table_name=table_name, data=instance_dict
    )
