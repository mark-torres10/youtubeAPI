from typing import Dict, List

from transformations.enrichment.mappings.models import MappedChannel, MappedEpisode


def get_channels_from_youtube_data() -> List[str]:
    """Get channels from YouTube data.

    Queries `channels` table to get info.

    TODO: should query only names? Or also names and other info?

    Maybe just names? So we can map these?
    """
    return [""]


def get_shows_from_spotify_data() -> List[str]:
    """Gets shows from Spotify data.

    Queries `spotify_show` table to get info.
    """
    return [""]


def get_youtube_videos(youtube_video_ids: List[str]) -> List[Dict]:
    """Given ids, get YouTube videos."""
    return [{}]


def get_spotify_episodes(spotify_episode_ids: List[str]) -> List[Dict]:
    """Given ids, get Spotify episodes."""
    return [{}]


def create_mapped_channel_instance(metadata: Dict) -> MappedChannel:
    return MappedChannel()


def create_mapped_episode_instance(metadata: Dict) -> MappedEpisode:
    return MappedEpisode()
