"""Maps YouTube videos and Spotify episodes."""
from datetime import datetime
from typing import Any, Dict, List, Union

from lib.log.logger import Logger
from transformations.enrichment import constants

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
    youtube_video: Dict,
    spotify_episode: Dict,
    allow_fuzzy_matching: bool = False
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
) -> Dict[str, str]:
    youtube_to_matching_spotify_episode: Dict[str, str] = {}
    # loop through all the YouTube videos, find most likely Spotify match
    for youtube_video in youtube_videos:
        youtube_id = youtube_video["video_id"]
        max_matching_score: float = 0.0
        max_matching_id: str = ""
        has_found_exact_match: bool = False
        for spotify_episode in spotify_episodes:
            spotify_id = spotify_episode["id"]
            match_dict = match_youtube_video_to_spotify_episode(
                youtube_video=youtube_video, spotify_episode=spotify_episode
            )
            match_type: str = match_dict["match_type"] # type: ignore
            match_score: float = match_dict["value"] # type: ignore
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
            youtube_to_matching_spotify_episode[youtube_id] = spotify_id
    return youtube_to_matching_spotify_episode


def find_most_likely_youtube_map_to_spotify_episodes(
    youtube_videos: List[Dict], spotify_episodes: List[Dict]
) -> Dict[str, str]:
    spotify_to_matching_youtube_video: Dict[str, str] = {}
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
            match_type: str = match_dict["match_type"] # type: ignore
            match_score: float = match_dict["value"] # type: ignore
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
            spotify_to_matching_youtube_video[spotify_id] = youtube_id
    return spotify_to_matching_youtube_video


def map_episodes(
    youtube_videos: List[Dict], spotify_episodes: List[Dict]
) -> List[Dict]:
    """Map a given channel's YouTube videos against possible Spotify podcast versions
    of those same videos.
    """
    youtube_to_matching_spotify_episode: Dict[str, str] = (
        find_most_likely_spotify_map_to_youtube_videos(
            youtube_videos=youtube_videos, spotify_episodes=spotify_episodes
        )
    )
    spotify_to_matching_youtube_video: Dict[str, str] = (
        find_most_likely_youtube_map_to_spotify_episodes(
            youtube_videos=youtube_videos, spotify_episodes=spotify_episodes
        )
    )

    mappings = []

    # check for bijective match. If so, add to mappings
    for youtube_id, spotify_id in youtube_to_matching_spotify_episode.items():
        if spotify_to_matching_youtube_video[spotify_id] == youtube_id:
            mappings.append({"youtube_id": youtube_id, "spotify_id": spotify_id})

    logger.info(
        f"From {len(youtube_videos)} and {len(spotify_episodes)}, created "
        f"{len(mappings)} mappings."
    )

    return mappings
