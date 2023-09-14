"""Mapping algorithm for pairing YouTube videos and Spotify episodes."""
from typing import Dict, List


def fuzzy_match_titles(
    youtube_video_title: str, spotify_episode_title: str
) -> float:
    """Performs fuzzy matching of the titles.
    
    Returns a float between 0 and 1 to indicate degree of matching.
    """
    pass


def channel_names_match(
    youtube_channel_name: str, spotify_podcast_name: str
) -> bool:
    """Checks to see if the YouTube and Spotify channel/podcast names match.
    
    This doesn't have to be fuzzy match; we should be able to use a hardcoded
    map in order to see if the names are actually matching.
    """
    pass


def fuzzy_match_descriptions(
    youtube_video_description: str,
    spotify_episode_description: str
) -> float:
    """Performs fuzzy matching of the titles.
    
    Returns a float between 0 and 1 to indicate degree of matching.
    """
    pass


def youtube_video_and_spotify_episode_posted_same_time(
    youtube_video_post_date: str,
    spotify_episode_post_date: str
) -> bool:
    """Get the difference in when the videos were posted and see if this
    falls in an acceptable range. Range could vary depending on variety of
    factors, but can be a constant as a first pass"""
    pass


def match_youtube_video_to_spotify_episode(
    youtube_video: Dict, spotify_episode: Dict
) -> float:
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
    """
    if not youtube_video_and_spotify_episode_posted_same_time(
        youtube_video_post_date="", spotify_episode_post_date=""
    ):
        return 0
    
    titles_match_score = fuzzy_match_titles(
        youtube_video_title="", spotify_episode_title=""
    )

    channel_names_match_score = channel_names_match(
        youtube_channel_name="", spotify_podcast_name=""
    )

    descriptions_match_score = fuzzy_match_descriptions(
        youtube_video_description="",
        spotify_episode_description=""
    )

    # it's likely that (assuming our algorithm works as intended) that
    # a proper mapping will lead to any of the scores being near 0, so if
    # we get that, then we can likely throw away the result.
    if any(
        [
            score == 0
            for score in [
                titles_match_score, channel_names_match_score,
                descriptions_match_score
            ]
        ]
    ):
        return 0

    return (
        titles_match_score
        + channel_names_match_score
        + descriptions_match_score
    )


def map_youtube_videos_to_spotify_podcasts(
    youtube_videos: List[Dict], spotify_episodes: List[Dict]
):
    """Map a given channel's YouTube videos against possible Spotify podcast versions
    of those same videos.

    Algorithm details:

    Loop through every video from a YouTube channel.
        For every video, compare against the possible Spotify podcast episodes.
        Most of these should score 0 since they'll be published at very
        different times. For the ones where it's not zero, we'll take the max.
        Record which Spotify podcast episode is the most likely match for a
        given YouTube video.
    Loop through every episode from a Spotify podcast show.
        Follow same algorithm as above.
        Record which YouTube video is the most likely match for a given
        Spotify podcast.
    If there's a reciprocated match between a given pair of YouTube video and
    Spotify podcast, return that pair as a match.
    """

    # TODO: make sure to have a tiebreaker scenario if scores match. Should
    # be resolved with a max? Or, take the one that has the closer date?
    youtube_to_matching_spotify_episode = {} # youtube_id: spotify_id
    spotify_to_matching_youtube_video = {} # spotify_id: youtube_id

    for youtube_video in youtube_videos:
        max_matching_score = 0
        max_matching_id = None
        for spotify_episode in spotify_episodes:
            matching_score = match_youtube_video_to_spotify_episode(
                youtube_video=youtube_video, spotify_episode=spotify_episode
            )
            if matching_score != 0 and matching_score > max_matching_score:
                max_matching_score = matching_score
                max_matching_id = spotify_episode["id"]
        if max_matching_id is not None:
            youtube_to_matching_spotify_episode[youtube_video["video_id"]] = (
                spotify_episode["id"]
            )

    for spotify_episode in spotify_episodes:
        max_matching_score = 0
        max_matching_id = None
        for youtube_video in youtube_videos:
            matching_score = match_youtube_video_to_spotify_episode(
                youtube_video=youtube_video, spotify_episode=spotify_episode
            )
            if matching_score != 0 and matching_score > max_matching_score:
                max_matching_score = matching_score
                max_matching_id = spotify_episode["id"]
        if max_matching_id is not None:
            spotify_to_matching_youtube_video[spotify_episode["id"]] = (
                youtube_video["video_id"]
            )

    mappings = []

    # TODO: should add the actual youtube_video and spotify_episode objects
    # so that when they're used, we don't have to rehydrate? Unless we pass
    # in objects to this function where the keys are the respective youtube or
    # spotify ids and the values are the data objects, so that we can keep the
    # id info and the data info.
    for youtube_id, spotify_id in youtube_to_matching_spotify_episode.items():
        if spotify_to_matching_youtube_video[spotify_id] == youtube_id:
            mappings.append({
                "youtube_id": youtube_id, "spotify_id": spotify_id
            })

    print(
        f"From {len(youtube_videos)} and {len(spotify_podcasts)}, created "
        f"{len(mappings)} mappings."
    )

    return mappings


def get_youtube_and_spotify_episodes_for_channel(
    channel_name: str
) -> Dict:
    """Get the YouTube videos and Spotify episodes for a given channel."""
    # TODO: implement
    return {
        "youtube_videos": [],
        "spotify_episodes": []
    }


def map_channel_youtube_spotify_content(channel_name: str) -> List[Dict]:
    data = get_youtube_and_spotify_episodes_for_channel(channel_name)
    youtube_videos = data["youtube_videos"]
    spotify_episodes = data["spotify_episodes"]
    mappings = map_youtube_videos_to_spotify_podcasts(
        youtube_videos=youtube_videos, spotify_episodes=spotify_episodes
    )
    return mappings
