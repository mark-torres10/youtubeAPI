from typing import Dict, List

import pandas as pd

from db.sql.constants import TABLE_NAME_TO_KEYS_MAP
from db.sql.helper import get_all_table_results_as_df
from transformations.enrichment.mappings.models import (
    MappedChannel, MappedChannelIntegrationMetadata, MappedEpisode,
    MappedEpisodeIntegrationMetadata
)


def get_map_tables_to_sqlite_data() -> Dict[str, pd.DataFrame]:
    """Get all the current data in the SQLite DB."""
    return {
        table_name: get_all_table_results_as_df(table_name)
        for table_name in TABLE_NAME_TO_KEYS_MAP.keys()
    }


def get_youtube_channel_info(
    channels_df: pd.DataFrame,
    cols_to_return: List[str] = ["channel_id", "channel_title"]
) -> List[Dict]:
    """Get all the YouTube channel names and ids. Returns unique names."""
    return channels_df[cols_to_return].to_dict(orient="records")


def get_spotify_show_info(
    spotify_df: pd.DataFrame,
    cols_to_return: List[str] = ["id", "show_title"]
) -> List[str]:
    """Get all the Spotify show names. Returns unique names."""
    return spotify_df[cols_to_return].to_dict(orient="records")


def create_mapped_channel_instance(metadata: Dict) -> MappedChannel:
    youtube_episode = MappedChannelIntegrationMetadata(
        id=metadata["youtube_channel_id"],
        name=metadata["youtube_channel_name"],
        episode_ids=metadata["youtube_episode_ids"]
    )
    spotify_episode = MappedChannelIntegrationMetadata(
        id=metadata["spotify_show_id"],
        name=metadata["spotify_show_name"],
        episode_ids=metadata["spotify_episode_ids"]
    )
    mapped_channel = MappedChannel(
        consolidated_name=metadata["consolidated_name"],
        youtube_channel=youtube_episode,
        spotify_channel=spotify_episode,
        last_updated_timestamp=metadata["last_updated_timestamp"]
    )
    return mapped_channel


def create_mapped_episode_instance(metadata: Dict) -> MappedEpisode:
    youtube_episode= MappedChannelIntegrationMetadata(
        metadata["youtube_episoode"]
    )
    spotify_episode = MappedChannelIntegrationMetadata(
        metadata["spotify_episode"]
    )
    mapped_episode = MappedEpisode(
        consolidated_name=metadata["consolidated_name"],
        mapped_channel_name=metadata["mapped_channel_name"],
        consolidated_description=metadata["consolidated_description"],
        youtube_episode=youtube_episode,
        spotify_episode=spotify_episode
    )
    return mapped_episode
