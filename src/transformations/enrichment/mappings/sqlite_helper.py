"""SQLite helper utilities for writing mapped data."""
from typing import Union

from db.sql import helper
from db.sql.helper import conn, cursor
from transformations.enrichment.helper import (
    flatten_mapped_channel, flatten_mapped_episode
)
from transformations.enrichment.mappings.models import MappedChannel, MappedEpisode


def write_mapped_data_to_db(instance: Union[MappedChannel, MappedEpisode]) -> None:
    """Writes either the MappedChannel or MappedEpisode instance to their
    respective SQLite tables."""
    table_name = instance.__table_name__
    instance_dict = (
        flatten_mapped_channel(instance) if isinstance(instance, MappedChannel)
        else flatten_mapped_episode(instance)
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
