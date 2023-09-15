from dataclasses import asdict
from typing import Dict

from integrations.youtube.models import (
    VideoMetadata, VideoStatistics, YoutubeChannel, YoutubeVideo
)


def create_channel_dataclass_instance(
    channel_metadata: Dict
) -> YoutubeChannel:
    channel = YoutubeChannel(
        channel_id=channel_metadata["channelId"],
        title=channel_metadata["title"],
        description=channel_metadata["description"],
        channel_title=channel_metadata["channelTitle"],
        publish_time=channel_metadata["publishTime"],
        published_at=channel_metadata["publishedAt"],
        synctimestamp=channel_metadata["synctimestamp"]
    )
    return channel


def create_video_dataclass_instance(video_metadata: Dict) -> YoutubeVideo:
    metadata = VideoMetadata(
        video_title=video_metadata["metadata"]["title"],
        channel_id=video_metadata["metadata"]["channelId"],
        channel_title=video_metadata["metadata"]["channelTitle"],
        category_id=video_metadata["metadata"]["categoryId"],
        default_audio_language=video_metadata["metadata"]["defaultAudioLanguage"], # noqa
        default_language=video_metadata["metadata"]["defaultLanguage"],
        description=video_metadata["metadata"]["description"],
        live_broadcast_content=video_metadata["metadata"]["liveBroadcastContent"], # noqa
        published_at=video_metadata["metadata"]["publishedAt"],
        tags=','.join(video_metadata["metadata"]["tags"])
    )
    statistics = VideoStatistics(
        view_count=video_metadata["statistics"]["viewCount"],
        like_count=video_metadata["statistics"]["likeCount"],
        favorite_count=video_metadata["statistics"]["favoriteCount"],
        comment_count=video_metadata["statistics"]["commentCount"]
    )    
    video = YoutubeVideo(
        video_id=video_metadata["video_id"],
        metadata=metadata,
        statistics=statistics,
        synctimestamp=video_metadata["synctimestamp"]
    )
    return video


def flatten_video(video: YoutubeVideo) -> Dict:
    """Flattens a `Video` instance."""
    return {
        **{
            "video_id": video.video_id,
            "synctimestamp": video.synctimestamp
        },
        **asdict(video.metadata),
        **asdict(video.statistics)
    }
