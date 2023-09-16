"""Maps YouTube videos and Spotify episodes."""
from datetime import datetime
from typing import Dict, List, Union

import pandas as pd

from lib.log.logger import Logger
from transformations.enrichment import constants
from transformations.enrichment.helper import create_mapped_episode_instance
from transformations.enrichment.models import MappedChannel, MappedEpisode

logger = Logger(__name__)


def titles_match(youtube_video_title: str, spotify_episode_title: str) -> bool:
    """Performs matching of the titles.

    Returns 1 for exact match. Otherwise, can return float between 0 and 1
    for fuzzy matching. Returns 0 if they clearly don't match.

    NOTE: first pass can be exact match.
    """
    return youtube_video_title == spotify_episode_title


def channel_names_match(youtube_channel_name: str, spotify_podcast_name: str) -> bool:
    """Checks to see if the YouTube and Spotify channel/podcast names match.

    This doesn't have to be fuzzy match; we should be able to use a hardcoded
    map in order to see if the names are actually matching (first pass can
    just be raw match).
    """
    return youtube_channel_name == spotify_podcast_name


def fuzzy_match_descriptions(
    youtube_video_description: str, spotify_episode_description: str
) -> bool:
    """Performs fuzzy matching of the titles.

    For first pass, can just do exact matching. Otherwise, later can do
    fuzzy matching.
    """
    return youtube_video_description == spotify_episode_description


def youtube_video_and_spotify_episode_posted_same_time(
    youtube_video_post_date: str, spotify_episode_post_date: str
) -> bool:
    """Get the difference in when the videos were posted and see if this
    falls in an acceptable range. Range could vary depending on variety of
    factors, but can be a constant as a first pass.

    Example:
    >> youtube_video_post_date = "2020-01-01T00:00:00Z"
    >> spotify_episode_post_date = "2020-01-01"
    >> youtube_video_and_spotify_episode_posted_same_time(
        youtube_video_post_date=youtube_video_post_date,
        spotify_episode_post_date=spotify_episode_post_date
    )
    True
    """
    # create datetime objects for each
    youtube_post_date_dt = datetime.strptime(
        youtube_video_post_date, "%Y-%m-%dT%H:%M:%SZ"
    )
    spotify_post_date_dt = datetime.strptime(spotify_episode_post_date, "%Y-%m-%d")

    # get the difference between the two, check if it is in acceptable range.
    num_hours_diff = abs(
        (youtube_post_date_dt - spotify_post_date_dt).total_seconds() / 3600
    )
    return num_hours_diff <= constants.POST_DATE_MAX_NUM_HOURS_DIFF


def exact_match_youtube_video_to_spotify_episode(
    youtube_video: Dict, spotify_episode: Dict
) -> float:
    """Tries an exact comparison between the YouTube and Spotify sources.
    If it can exactly tell that they are identical, then it returns 1.
    If it can exactly tell that they are definitely NOT identical, then it
    returns -1. Else it returns 0.
    """

    # if they're not posted at the same time (or around the same time),
    # we will assume they're not the same.
    if not youtube_video_and_spotify_episode_posted_same_time(
        youtube_video_post_date=youtube_video["published_at"],
        spotify_episode_post_date=spotify_episode["release_date"],
    ):
        return -1.0

    # if podcast name plus episode name are the same, then we can assume
    # that they are the same.
    if channel_names_match(
        youtube_channel_name=youtube_video["channel_title"],
        spotify_podcast_name=spotify_episode["show_name"],
    ) and titles_match(
        youtube_video_title=youtube_video["video_title"],
        spotify_episode_title=spotify_episode["name"],
    ):
        return 1.0
    return 0


def fuzzy_match_youtube_video_to_spotify_episode(
    youtube_video: Dict, spotify_episode: Dict
) -> float:
    """Perform fuzzy matching between YouTube and Spotify sources.

    Returns a float between 0 and 1 that is a confidence score of the
    linkage.
    """
    titles_match_score = float(
        titles_match(
            youtube_video_title=youtube_video["video_title"],
            spotify_episode_title=spotify_episode["name"],
        )
    )

    channel_names_match_score = float(
        channel_names_match(
            youtube_channel_name=youtube_video["channel_title"],
            spotify_podcast_name=spotify_episode["show_name"],
        )
    )

    descriptions_match_score = float(
        fuzzy_match_descriptions(
            youtube_video_description="", spotify_episode_description=""
        )
    )

    # it's likely that (assuming our algorithm works as intended) that
    # a proper mapping will lead to any of the scores being near 0, so if
    # we get that, then we can likely throw away the result.
    if any(
        [
            score == 0
            for score in [
                titles_match_score,
                channel_names_match_score,
                descriptions_match_score,
            ]
        ]
    ):
        return 0.0

    return titles_match_score + channel_names_match_score + descriptions_match_score


def match_youtube_video_to_spotify_episode(
    youtube_video: Dict, spotify_episode: Dict, allow_fuzzy_matching: bool = False
) -> Dict[str, Union[str, float]]:
    """Performs a matching between a YouTube video and Spotify episode, to
    get the likelihood (a float between 0 and 1) that they should be
    mapped together.

    Algorithm details:
    1. It's likely that a YouTube and a Spotify version of the same podcast
    episode were posted at (around) the same time. Therefore, we can check to
    see if the YouTube video and Spotify podcast were. As a first pass, we can
    reasonably assume that if they were posted at vastly different dates, they
    likely aren't the same.
    2. If they were posted at around the same time, do other matching.

    Returns a dictionary of the following format:
    {
        "match_type": ["exact", "fuzzy"],
        "value": float between 0 and 1 (For exact, 0 if no match, 1 if match)
    }
    """
    is_exact_match = exact_match_youtube_video_to_spotify_episode(
        youtube_video=youtube_video, spotify_episode=spotify_episode
    )
    match_type: str = "exact" if is_exact_match else "fuzzy"
    if is_exact_match:
        return {
            "match_type": match_type,
            "value": is_exact_match,  # 1 if exact match, -1 if exact no match
        }

    if allow_fuzzy_matching:
        fuzzy_match_score = fuzzy_match_youtube_video_to_spotify_episode(
            youtube_video=youtube_video, spotify_episode=spotify_episode
        )
        return {"match_type": match_type, "value": fuzzy_match_score}
    else:
        return {"match_type": match_type, "value": 0.0}


def find_most_likely_spotify_map_to_youtube_videos(
    youtube_videos: List[Dict], spotify_episodes: List[Dict]
) -> Dict[str, Dict]:
    youtube_to_matching_spotify_episode: Dict[str, Dict] = {}
    # loop through all the YouTube videos, find most likely Spotify match
    for youtube_video in youtube_videos:
        youtube_id = youtube_video["video_id"]
        max_matching_score: float = 0.0
        max_matching_id: str = ""
        has_found_exact_match: bool = False
        for spotify_episode in spotify_episodes:
            spotify_id: str = spotify_episode["id"]
            spotify_episode_name: str = spotify_episode["name"]
            match_dict = match_youtube_video_to_spotify_episode(
                youtube_video=youtube_video, spotify_episode=spotify_episode
            )
            match_type: str = match_dict["match_type"]  # type: ignore
            match_score: float = match_dict["value"]  # type: ignore
            if match_type == "exact":
                # found exact match
                if match_score == 1.0:
                    has_found_exact_match = True
                    max_matching_id = spotify_id
                # skip if definitely not a match.
                elif match_score == -1.0:
                    continue
            else:
                if match_score != 0.0 and match_score > max_matching_score:
                    max_matching_score = match_score
                    max_matching_id = spotify_id
            if has_found_exact_match:
                break
        if max_matching_id is not None:
            youtube_to_matching_spotify_episode[youtube_id] = {
                "matching_id": spotify_id,
                "matching_name": spotify_episode_name,
                "matching_description": spotify_episode["description"],  # noqa
                "original_id": youtube_id,
                "original_name": youtube_video["video_title"],
                "original_description": youtube_video["description"],
            }
    return youtube_to_matching_spotify_episode


def find_most_likely_youtube_map_to_spotify_episodes(
    youtube_videos: List[Dict], spotify_episodes: List[Dict]
) -> Dict[str, Dict]:
    spotify_to_matching_youtube_video: Dict[str, Dict] = {}
    # loop through all the Spotify episodes, find most likely YouTube match
    for spotify_episode in spotify_episodes:
        spotify_id = spotify_episode["id"]
        max_matching_score: float = 0.0
        max_matching_id: str = ""
        has_found_exact_match: bool = False
        for youtube_video in youtube_videos:
            youtube_id = youtube_video["video_id"]
            match_dict = match_youtube_video_to_spotify_episode(
                youtube_video=youtube_video, spotify_episode=spotify_episode
            )
            match_type: str = match_dict["match_type"]  # type: ignore
            match_score: float = match_dict["value"]  # type: ignore
            if match_type == "exact":
                # found exact match
                if match_score == 10:
                    has_found_exact_match = True
                    max_matching_id = youtube_id
                # skip if definitely not a match.
                elif match_score == -1.0:
                    continue
            else:
                if match_score != 0.0 and match_score > max_matching_score:
                    max_matching_score = match_score
                    max_matching_id = youtube_id
            if has_found_exact_match:
                break
        if max_matching_id is not None:
            spotify_to_matching_youtube_video[spotify_id] = {
                "matching_id": youtube_id,
                "matching_name": youtube_video["video_title"],
                "matching_description": youtube_video["description"],
                "original_id": spotify_id,
                "original_name": spotify_episode["name"],
                "original_ddescription": spotify_episode["description"],
            }
    return spotify_to_matching_youtube_video


def get_episode_id_to_channel_id_map(
    mapped_channels: List[MappedChannel],
) -> Dict[str, Dict[str, Dict]]:
    """
    Returns a map of the episode ID to the channel ID

    Returns a dictionary of the following format:
    {
        "youtube": {
            "episode_id": {
                "mapped_channel_name": "",
                "integration_channel_id": ""
            }
        },
        "spotify": {
            "episode_id": {
                "mapped_channel_name": "",
                "integration_channel_id": ""
            }
        }
    }
    """
    youtube_episode_id_to_channel_id = {}
    spotify_episode_id_to_channel_id = {}
    for mapped_channel in mapped_channels:
        mapped_channel_name = mapped_channel.consolidated_name
        youtube_channel_info = mapped_channel.youtube_channel
        youtube_channel_id = youtube_channel_info.id
        yotube_episode_ids = youtube_channel_info.episode_ids
        for youtube_episode_id in yotube_episode_ids:
            youtube_episode_id_to_channel_id[youtube_episode_id] = {
                "mapped_channel_name": mapped_channel_name,
                "integration_channel_id": youtube_channel_id,
            }

        spotify_channel_info = mapped_channel.spotify_channel
        spotify_channel_id = spotify_channel_info.id
        spotify_episode_ids = spotify_channel_info.episode_ids
        for spotify_episode_id in spotify_episode_ids:
            spotify_episode_id_to_channel_id[spotify_episode_id] = {
                "mapped_channel_name": mapped_channel_name,
                "integration_channel_id": spotify_channel_id,
            }

    return {
        "youtube": youtube_episode_id_to_channel_id,
        "spotify": spotify_episode_id_to_channel_id,
    }


def get_consolidate_episode_name(
    youtube_episode_name: str, spotify_episode_name: str
) -> str:
    """Get consolidated episode name. For now, use Spotify episode name."""
    if youtube_episode_name != spotify_episode_name:
        logger.info(
            "Youtube episode name != Spotify episode name",
            youtube_episode_name=youtube_episode_name,
            spotify_episode_name=spotify_episode_name,
        )
    return spotify_episode_name


def get_consolidated_description(
    youtube_episode_description: str, spotify_episode_description: str
) -> str:
    """Get consolidated description. For now, use Spotify episode description."""
    if youtube_episode_description != spotify_episode_description:
        logger.info(
            "Youtube episode description != Spotify episode description",
            youtube_episode_description=youtube_episode_description,
            spotify_episode_description=spotify_episode_description,
        )
    return spotify_episode_description


def get_consolidated_mapped_channel_name(
    youtube_channel_name: str, spotify_channel_name: str
) -> str:
    """Get consolidated channel name. For now, use Spotify channel name."""
    if youtube_channel_name != spotify_channel_name:
        logger.info(
            "Youtube channel name != Spotify channel name",
            youtube_channel_name=youtube_channel_name,
            spotify_channel_name=spotify_channel_name,
        )
    return spotify_channel_name


def create_mapped_episode_metadata(
    mapping: Dict[str, str],
    youtube_episode_id_to_channel_id_map: Dict[str, Dict],
    spotify_episode_id_to_channel_id_map: Dict[str, Dict],
) -> Dict:
    """Given the mapped metadata with the integration id and episode name,
    hydrate with more information and create the mapped episode metadata.

    Things to add:
    - consolidated name
    - consolidated description
    - channel id
    """
    consolidated_name = get_consolidate_episode_name(
        youtube_episode_name=mapping["youtube_episode_name"],
        spotify_episode_name=mapping["spotify_episode_name"],
    )
    consolidated_description = get_consolidated_description(
        youtube_episode_description=mapping["youtube_description"],
        spotify_episode_description=mapping["spotify_description"],
    )
    youtube_episode_id = mapping["youtube_id"]
    spotify_episode_id = mapping["spotify_id"]
    youtube_channel_data = youtube_episode_id_to_channel_id_map[youtube_episode_id]
    spotify_channel_data = spotify_episode_id_to_channel_id_map[spotify_episode_id]

    mapped_channel_name = get_consolidated_mapped_channel_name(
        youtube_channel_name=youtube_channel_data["mapped_channel_name"],
        spotify_channel_name=spotify_channel_data["mapped_channel_name"],
    )

    youtube_episode_data = {
        "id": youtube_episode_id,
        "channel_id": youtube_channel_data["integration_channel_id"],
        "name": mapping["youtube_episode_name"],
    }

    spotify_episode_data = {
        "id": spotify_episode_id,
        "channel_id": spotify_channel_data["integration_channel_id"],
        "name": mapping["spotify_episode_name"],
    }

    return {
        "consolidated_name": consolidated_name,
        "mapped_channel_name": mapped_channel_name,
        "consolidated_description": consolidated_description,
        "youtube_episode": youtube_episode_data,
        "spotify_episode": spotify_episode_data,
    }


def map_episodes(
    youtube_videos: List[Dict],
    spotify_episodes: List[Dict],
    mapped_channels: List[MappedChannel],
) -> List[Dict]:
    """Map a given channel's YouTube videos against possible Spotify podcast versions
    of those same videos.
    """
    youtube_to_matching_spotify_episode: Dict[
        str, Dict[str, str]
    ] = find_most_likely_spotify_map_to_youtube_videos(
        youtube_videos=youtube_videos, spotify_episodes=spotify_episodes
    )
    spotify_to_matching_youtube_video: Dict[
        str, Dict[str, str]
    ] = find_most_likely_youtube_map_to_spotify_episodes(
        youtube_videos=youtube_videos, spotify_episodes=spotify_episodes
    )

    mappings: List[Dict] = []

    # check for bijective match. If so, add to mappings
    for (
        youtube_id,
        matching_spotify_data,
    ) in youtube_to_matching_spotify_episode.items():  # noqa
        spotify_id = matching_spotify_data["matching_id"]
        spotify_episode_name = matching_spotify_data["matching_name"]
        spotify_description = matching_spotify_data["matching_description"]
        if spotify_to_matching_youtube_video[spotify_id]["matching_id"] == (youtube_id):
            mappings.append(
                {
                    "youtube_id": youtube_id,
                    "spotify_id": spotify_id,
                    "youtube_episode_name": matching_spotify_data[
                        "original_name"
                    ],  # noqa
                    "spotify_episode_name": spotify_episode_name,
                    "youtube_description": matching_spotify_data[
                        "original_description"
                    ],  # noqa
                    "spotify_description": spotify_description,
                }
            )

    logger.info(
        f"From {len(youtube_videos)} and {len(spotify_episodes)}, created "
        f"{len(mappings)} mappings."
    )

    episode_id_to_channel_id_map = get_episode_id_to_channel_id_map(
        mapped_channels=mapped_channels
    )
    youtube_episode_id_to_channel_id_map = episode_id_to_channel_id_map[
        "youtube"
    ]  # noqa
    spotify_episode_id_to_channel_id_map = episode_id_to_channel_id_map[
        "spotify"
    ]  # noqa

    # hydrate the youtube/spotify ids with the channel information
    mapped_episode_metadatas = [
        create_mapped_episode_metadata(
            mapping=mapping,
            youtube_episode_id_to_channel_id_map=(youtube_episode_id_to_channel_id_map),
            spotify_episode_id_to_channel_id_map=(spotify_episode_id_to_channel_id_map),
        )
        for mapping in mappings
    ]

    mapped_episodes: List[MappedEpisode] = [
        create_mapped_episode_instance(episode_metadata)
        for episode_metadata in mapped_episode_metadatas
    ]

    return mapped_episodes
