"""Wrapper dataclass to store channel information."""
from dataclass import dataclass
from datetime import datetime
from typing import Dict

@dataclass
class Channel:
    """Class that keeps track of information for a given YouTube channel.
    
    Specifically, stores channel-level metadata as well as information
    about the videos on the channel.
    """
    __tablename__ = 'channels'

    id: int
    channel_handle: str
    channel_id: str
    statistics_per_latest_videos: Dict
    sync_timestamp: datetime


@dataclass
class Video:
    """Class that stores statistics about a given video."""
    __tablename__ = 'videos'
    id: int
    video_id: str
    parent_channel_id: str
    title: str
    description: str
    published_at: datetime
    views: int
    likes: int
    dislikes: int
    comments: int
    sync_timestamp: datetime
