"""Wrapper dataclass to store Spotify data."""
from dataclasses import dataclass, fields
from typing import List


@dataclass
class SpotifyEpisode:
    """Class that keeps track of episode-specific information for an episode
    of a Spotify podcast/show.
    
    See https://developer.spotify.com/documentation/web-api/reference/get-a-show
    and https://developer.spotify.com/documentation/web-api/reference/get-a-shows-episodes
    """ # noqa
    __table_name__ = "spotify_episode"
    id: str # primary key
    show_id: str # foreign key
    audio_preview_url: str
    description: str
    html_description: str
    duration_ms: int
    explicit: bool
    href: str
    is_externally_hosted: bool
    is_playable: bool
    languages: List[str]
    name: str
    release_date: str
    release_date_precision: str
    type: str # only 1 possible value, "episode"
    uri: str
    synctimestamp: str


@dataclass
class SpotifyShow:
    """Class that keeps track of metadata for a given Spotify podcast/show.
    
    Reference: https://developer.spotify.com/documentation/web-api/reference/get-a-show
    """ # noqa
    __table_name__ = "spotify_show"
    id: str # primary key
    available_markets: List[str]
    copyrights: List[str]
    description: str
    explicit: bool
    href: str
    html_description: str
    is_externally_hosted: bool
    languages: List[str]
    media_type: str
    name: str
    publisher: str
    type: str # only 1 possible value, "show"
    uri: str
    total_episodes: int
    episode_ids: List[str] # contains the IDs of the episodes
    synctimestamp: str


def get_all_attributes_in_dataclass(cls) -> List[str]:
    return [field.name for field in fields(cls)]
