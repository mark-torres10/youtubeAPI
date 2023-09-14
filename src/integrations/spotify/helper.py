from typing import Dict

from integrations.spotify.constants import SPOTIFY_LIST_STRING_FIELDS
from integrations.spotify.models import (
    get_all_attributes_in_dataclass, SpotifyEpisode, SpotifyShow
)


def create_spotify_episode_instance(
    metadata: Dict, show_id: str
) -> SpotifyEpisode:
    episode = SpotifyEpisode(
        id=metadata["id"],
        show_id=show_id,
        audio_preview_url=metadata["audio_preview_url"],
        description=metadata["description"],
        html_description=metadata["html_description"],
        duration_ms=metadata["duration_ms"],
        explicit=metadata["explicit"],
        href=metadata["href"],
        is_externally_hosted=metadata["is_externally_hosted"],
        is_playable=metadata["is_playable"],
        languages=metadata["languages"],
        name=metadata["name"],
        release_date=metadata["release_date"],
        release_date_precision=metadata["release_date_precision"],
        type=metadata["type"],
        uri=metadata["uri"],
        synctimestamp=metadata["synctimestamp"]
    )
    return episode


def create_spotify_show_instance(metadata: Dict) -> SpotifyShow:
    show = SpotifyShow(
        id=metadata["id"],
        available_markets=metadata["available_markets"],
        copyrights=metadata["copyrights"],
        description=metadata["description"],
        explicit=metadata["explicit"],
        href=metadata["href"],
        html_description=metadata["html_description"],
        is_externally_hosted=metadata["is_externally_hosted"],
        languages=metadata["languages"],
        media_type=metadata["media_type"],
        name=metadata["name"],
        publisher=metadata["publisher"],
        type=metadata["type"],
        uri=metadata["uri"],
        total_episodes=metadata["total_episodes"],
        episode_ids=[
            episode["id"] for episode in metadata["episodes"]["items"]
        ],
        synctimestamp=metadata["synctimestamp"]
    )
    return show

def flatten_spotify_episode(episode: SpotifyEpisode) -> Dict:
    """Flatten a `SpotifyEpisode` instance."""
    return {
        field: (
            getattr(episode, field)
            if field not in SPOTIFY_LIST_STRING_FIELDS
            else ",".join(getattr(episode, field))
        )
        for field in get_all_attributes_in_dataclass(SpotifyEpisode)
    }


def flatten_spotify_show(show: SpotifyShow) -> Dict:
    """Flatten a `SpotifyShow` instance."""
    return {
        field: (
            getattr(show, field)
            if field not in SPOTIFY_LIST_STRING_FIELDS
            else ",".join(getattr(show, field))
        )
        for field in get_all_attributes_in_dataclass(SpotifyShow)
    }
