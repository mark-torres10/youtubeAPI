"""Wrapper dataclass to store YouTube data."""
from dataclasses import dataclass

@dataclass
class Channel:
    """Class that keeps track of metadata for a given YouTube channel."""
    __table_name__ = "channels"
    channel_id: str
    title: str
    description: str
    channel_title: str
    publish_time: str
    published_at: str
    synctimestamp: str


@dataclass
class VideoMetadata:
    video_title: str
    channel_id: str
    channel_title: str
    category_id: str
    default_audio_language: str
    default_language: str
    description: str
    live_broadcast_content: str
    published_at: str
    tags: str


@dataclass
class VideoStatistics:
    view_count: int
    like_count: int
    favorite_count: int
    comment_count: int


@dataclass
class Video:
    """Class that stores statistics about a given video."""
    __table_name__ = "videos"
    video_id: str
    metadata: VideoMetadata
    statistics: VideoStatistics
    synctimestamp: str
