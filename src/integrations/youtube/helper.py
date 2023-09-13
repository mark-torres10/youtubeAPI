from typing import Dict

from integrations.youtube.models import (
    Channel, Video, VideoMetadata, VideoStatistics
)
from lib.constants import (
    CURRENT_SYNCTIMESTAMP, YOUTUBE_CHANNEL_ID, YOUTUBE_CHANNEL_NAME
)

# NOTE: for testing, just one channel. But could easily add more.
MAP_CHANNEL_HANDLE_TO_ID = {
    YOUTUBE_CHANNEL_NAME: YOUTUBE_CHANNEL_ID
}

METADATA_TO_HYDRATE = {
    "synctimestamp": CURRENT_SYNCTIMESTAMP
}


def hydrate_with_metadata(data: Dict) -> Dict:
    """Hydrate sync data with metadata."""
    return {
        **data,
        **METADATA_TO_HYDRATE
    }


def create_channel_dataclass_instance(channel_metadata: Dict) -> Channel:
    channel = Channel(
        channel_id=channel_metadata["channelId"],
        title=channel_metadata["title"],
        description=channel_metadata["description"],
        channel_title=channel_metadata["channelTitle"],
        publish_time=channel_metadata["publishTime"],
        published_at=channel_metadata["publishedAt"],
        synctimestamp=channel_metadata["synctimestamp"]
    )
    return channel


def create_video_dataclass_instance(video_metadata: Dict) -> Video:
    metadata = VideoMetadata(
        video_title=video_metadata["metadata"]["title"],
        channel_id=video_metadata["metadata"]["channelId"],
        channel_title=video_metadata["metadata"]["channelTitle"],
        default_audio_language=video_metadata["metadata"]["defaultAudioLanguage"], # noqa
        default_language=video_metadata["metadata"]["defaultLanguage"],
        description=video_metadata["metadata"]["description"],
        live_broadcast_content=video_metadata["metadata"]["liveBroadcastContent"], # noqa
        published_at=video_metadata["metadata"]["publishedAt"],
        tags=video_metadata["metadata"]["tags"]
    )
    statistics = VideoStatistics(
        view_count=video_metadata["statistics"]["viewCount"],
        like_count=video_metadata["statistics"]["likeCount"],
        favorite_count=video_metadata["statistics"]["favoriteCount"],
        comment_count=video_metadata["statistics"]["commentCount"]
    )    
    video = Video(
        video_id=video_metadata["video_id"],
        metadata=metadata,
        statistics=statistics,
        synctimestamp=video_metadata["synctimestamp"]
    )
    return video


def flatten_video(video: Video) -> Dict:
    """Flattens a `Video` instance."""
    flattened_video = {
        "video_id": video.video_id,
        "video_title": video.metadata.video_title,
        "channel_id": video.metadata.channel_id,
        "channel_title": video.metadata.channel_title,
        "category_id": video.metadata.category_id,
        "default_audio_language": video.metadata.default_audio_language,
        "default_language": video.metadata.default_language,
        "description": video.metadata.description,
        "live_broadcast_content": video.metadata.live_broadcast_content,
        "published_at": video.metadata.published_at,
        "tags": ",".join(video.metadata.tags),
        "view_count": video.statistics.view_count,
        "like_count": video.statistics.like_count,
        "favorite_count": video.statistics.favorite_count,
        "comment_count": video.statistics.comment_count,
        "synctimestamp": video.synctimestamp,
    }
    return flattened_video
