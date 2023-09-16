"""Maps YouTube and Spotify channels."""
from typing import Dict, List, Literal

import pandas as pd

from lib.constants import CURRENT_SYNCTIMESTAMP
from transformations.enrichment.helper import (
    create_mapped_channel_instance,
    get_spotify_show_info,
    get_youtube_channel_info,
)


YOUTUBE_CHANNEL_TO_SPOTIFY_SHOW_MAPPING = {"Andrew Huberman": "Huberman Lab"}

SPOTIFY_SHOW_TO_YOUTUBE_CHANNEL_MAP = {
    spotify_name: youtube_name
    for youtube_name, spotify_name in YOUTUBE_CHANNEL_TO_SPOTIFY_SHOW_MAPPING.items()
}


def return_consolidated_channel_name(
    channel_name: str, integration: Literal["spotify", "youtube"]
) -> str:
    """Returns the consolidated channel name."""
    return (
        channel_name
        if integration == "spotify"
        else YOUTUBE_CHANNEL_TO_SPOTIFY_SHOW_MAPPING[channel_name]
    )


def consolidate_channel_metadata(
    channel_info: Dict, integration: Literal["spotify", "youtube"]
) -> Dict:
    """Consolidate the channel metadata from both the YouTube and Spotify
    versions into one unified version.

    For now, we can just use the Spotify one by default.

    Returns a list of the following dict:
    {
        "consolidated_name": str,
        "youtube_channel_name": str,
        "spotify_show_name": str,
        "last_updated_timestamp": str (current timestamp)
    }
    """
    youtube_name = (
        channel_info["channel_title"]
        if integration == "youtube"
        else SPOTIFY_SHOW_TO_YOUTUBE_CHANNEL_MAP[channel_info["show_title"]]
    )
    spotify_name = (
        channel_info["show_title"]
        if integration == "spotify"
        else YOUTUBE_CHANNEL_TO_SPOTIFY_SHOW_MAPPING[channel_info["channel_title"]]
    )
    return {
        "consolidated_name": spotify_name,
        "youtube_channel_name": youtube_name,
        "spotify_show_name": spotify_name,
        "last_updated_timestamp": CURRENT_SYNCTIMESTAMP,
    }


def get_map_channel_to_episode_ids(
    youtube_videos_df: pd.DataFrame, spotify_episodes_df: pd.DataFrame
) -> Dict[str, Dict[str, List[str]]]:
    """Get a mapping of channel name to episode ids.

    Returns a dictionary of the following format:

    {
        "youtube": {
            "channel-id": ["episode-id-1", "episode-id-2"]
        },
        "spotify": {
            "channel-id": ["episode-id-1", "episode-id-2"]
        }
    }
    """
    youtube_channel_id_to_episode_ids_map: Dict[str, List[str]] = {}
    spotify_channel_id_to_episode_ids_map: Dict[str, List[str]] = {}

    for _, row in youtube_videos_df.iterrows():
        channel_id = row["channel_id"]
        episode_id = row["video_id"]
        if channel_id not in youtube_channel_id_to_episode_ids_map:
            youtube_channel_id_to_episode_ids_map[channel_id] = []
        youtube_channel_id_to_episode_ids_map[channel_id].append(episode_id)

    for _, row in spotify_episodes_df.iterrows():
        channel_id = row["show_id"]
        episode_id = row["id"]
        if channel_id not in spotify_channel_id_to_episode_ids_map:
            spotify_channel_id_to_episode_ids_map[channel_id] = []
        spotify_channel_id_to_episode_ids_map[channel_id].append(episode_id)

    return {
        "youtube": youtube_channel_id_to_episode_ids_map,
        "spotify": spotify_channel_id_to_episode_ids_map,
    }


def map_channels(
    youtube_channels_df: pd.DataFrame,
    spotify_shows_df: pd.DataFrame,
    youtube_videos_df: pd.DataFrame,
    spotify_episodes_df: pd.DataFrame,
) -> List[Dict]:
    """Map YouTube and Spotify channels."""

    youtube_channel_info_list = get_youtube_channel_info(youtube_channels_df)
    spotify_show_info_list = get_spotify_show_info(spotify_shows_df)

    consolidated_name_to_channel_metadata_map: Dict[str, Dict] = {}

    # create consolidated metadata, starting with youtube data
    for youtube_channel in youtube_channel_info_list:
        consolidated_name = return_consolidated_channel_name(
            youtube_channel["channel_title"], "youtube"
        )
        channel_metadata = consolidate_channel_metadata(youtube_channel, "youtube")
        youtube_channel_id = youtube_channel["channel_id"]
        channel_metadata["youtube_channel_id"] = youtube_channel_id
        consolidated_name_to_channel_metadata_map[consolidated_name] = channel_metadata

    # enrich consolidated metadata with spotify data
    for spotify_show in spotify_show_info_list:
        consolidated_name = return_consolidated_channel_name(
            spotify_show["show_title"], "spotify"
        )
        spotify_show_id = spotify_show["id"]
        channel_metadata["spotify_show_id"] = spotify_show_id
        consolidated_name_to_channel_metadata_map[consolidated_name][
            "spotify_show_id"
        ] = channel_metadata  # noqa

    consolidated_metadata: List[Dict] = list(
        consolidated_name_to_channel_metadata_map.values()
    )

    # add the episode ids to the consolidated metadata
    map_channel_to_episode_ids = get_map_channel_to_episode_ids(
        youtube_videos_df, spotify_episodes_df
    )

    youtube_channel_to_episode_ids_map = map_channel_to_episode_ids["youtube"]
    spotify_channel_to_episode_ids_map = map_channel_to_episode_ids["spotify"]

    mapped_channel_metadata = []

    for channel_metadata in consolidated_metadata:
        youtube_channel_id = channel_metadata["youtube_channel_id"]
        spotify_show_id = channel_metadata["spotify_show_id"]
        channel_metadata["youtube_episode_ids"] = youtube_channel_to_episode_ids_map[
            youtube_channel_id
        ]
        channel_metadata["spotify_episode_ids"] = spotify_channel_to_episode_ids_map[
            spotify_show_id
        ]
        mapped_channel_metadata.append(channel_metadata)

    # create mapped channel instances
    mapped_channels = [
        create_mapped_channel_instance(channel_metadata)
        for channel_metadata in mapped_channel_metadata
    ]

    return mapped_channels
