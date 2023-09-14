"""SQLite helper utilities for writing YouTube data."""
from typing import Union

import pandas as pd

from db.sql.helper import (
    conn, cursor, check_if_table_exists, create_table, write_to_database
)
from integrations.youtube import helper
from integrations.youtube.models import Channel, Video


def write_youtube_data_to_db(instance: Union[Channel, Video]) -> None:
    """Writes either the Channel or Video instance to their respective
    SQLite tables."""
    table_name = instance.__table_name__
    if isinstance(instance, Video):
        instance_dict = helper.flatten_video(instance)
    else:
        instance_dict = instance.__dict__
    instance_dict.pop('__table_name__', None)

    if not check_if_table_exists(table_name):
        create_table(table_name)

    write_to_database(
        conn=conn, cursor=cursor, table_name=table_name, data=instance_dict
    )


def get_all_table_results_as_df(table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    return df
