"""Access to YouTube API.

Auth details: https://developers.google.com/youtube/v3/quickstart/python
Helpful start resource: https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
API start docs: https://developers.google.com/youtube/v3/docs/?apix=true#Channels
Full API docs: https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/
""" # noqa
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import Dict, List, Optional

from googleapiclient.discovery import build

load_dotenv(Path("../../../.env"))

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube_client: googleapiclient.discover.resource = (
    build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
)

class YoutubeClient:
    def __init__(self):
        self.client: googleapiclient.discover.resource = (
            build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        )


    def get_channel_id_from_handle(self, handle: str) -> str:
        response = self.client.channels().list(
            part="id",
            forUsername=handle
        ).execute()
        return response["etag"]
    
    
    def get_video_details_from_id(
        self, video_id: str, part_str: Optional[str] = "snippet,statistics"
    ) -> Dict:
        response = self.client.videos().list(
            part=part_str,
            id=video_id
        ).execute()
        return response


    def get_videos_for_channel(
        self,
        handle: Optional[str] = None,
        channel_id: Optional[str] = None,
        max_results: Optional[int] = 10,
        order: Optional[str] = "date" # TODO: how else it can be sorted?
    ) -> List[str]:
        if handle is None and channel_id is None:
            raise ValueError("One of handle or channel ID must be given.")
    
        if handle and not channel_id:
            channel_id = self.get_channel_id_from_handle(handle)

        response = self.client.search().list(
            part="id",
            channelId=channel_id,
            maxResults=max_results,
            order=order,
            type="video"
        )

        video_ids = [
            item['id']['videoId'] for item in response.get('items', [])
        ]

        return video_ids


    def get_latest_video_stats_for_channel_by_video(
        self,
        handle: Optional[str] = None,
        channel_id: Optional[str] = None,
        max_results: Optional[int] = 10,
        order: Optional[str] = "date"
    ) -> Dict:
        """Maps the video ID to statistics about the video."""
        video_ids = self.get_videos_for_channel(
            handle=handle, channel_id=channel_id, max_results=max_results,
            order=order
        )

        video_id_to_info_map = {}

        for video_id in video_ids:
            video_response = self.get_video_details_from_id(
                video_id=video_id
            )
            item = video_response['items'][0]
            snippet = item['snippet']
            statistics = item['statistics']

            # Extract relevant details
            video_info = {
                'video_id': video_id,
                'title': snippet['title'],
                'description': snippet.get('description', ''),
                'published_at': snippet['publishedAt'],
                'views': int(statistics.get('viewCount', 0)),
                'likes': int(statistics.get('likeCount', 0)),
                'dislikes': int(statistics.get('dislikeCount', 0)),
                'comments': int(statistics.get('commentCount', 0))
            }
        
            video_id_to_info_map[video_id] = video_info
        
        return video_id_to_info_map
