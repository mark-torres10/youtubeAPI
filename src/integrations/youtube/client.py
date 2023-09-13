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
from googleapiclient.errors import HttpError

from integrations.youtube import helper

load_dotenv(Path("../../../.env"))

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube_client = (
    build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
)

def manage_rate_limit_throttling(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except HttpError as e:
            if e.resp.status == 429:
                # TODO: investigate rate limits to figure out backoff strategy
                #print("Rate limit exceeded. Waiting and retrying...")
                #time.sleep(60)  # Sleep for 60 seconds (adjust as needed)
                return wrapper(*args, **kwargs)  # Retry the function
            else:
                # Handle other HTTP errors here, e.g., log or raise an exception
                print(f"HTTP error: {e}")
                return {"error": f"HTTP error: {e}"}
    return wrapper

class YoutubeClient:
    def __init__(self):
        self.client: googleapiclient.discovery.resource = (
            build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        )

    # https://developers.google.com/youtube/v3/guides/working_with_channel_ids
    def get_channel_id_from_handle(self, handle: str) -> str:    
        """Gets channel ID from a handle.
        
        NOTE: need to get this implementing, but API docs seem to be misleading
        """    
        response = self.client.channels().list(
            part="id",
            forUsername=handle
        ).execute()
        return response["etag"]
    
    # # https://developers.google.com/youtube/v3/guides/working_with_channel_ids
    @manage_rate_limit_throttling
    def get_channel_metadata(self, channel_name: str) -> str:
        """Retrieve channel information from the channel name.
        
        NOTE: this approach returns multiple possibilities. Ideally would use
        the channel tags instead. For a first pass, just returning the
        first result, since this will give us the most likely result.
        """
        response = self.client.search().list(
            part="snippet", type="channel", q=channel_name
        ).execute()

        metadata = response["items"][0]["snippet"]

        return {**metadata, **helper.METADATA_TO_HYDRATE}

    @manage_rate_limit_throttling
    def get_video_ids_for_channel(
        self,
        channel_id: str,
        max_results_total: Optional[int] = 20,
        max_results_per_query: Optional[int] = 20,
        order: Optional[str] = "date" # TODO: how else it can be sorted?
    ) -> List[str]:
        """Get all the videos that are available for a given channel.
        
        TODO: for a data pipeline, we would only get the videos that are new.
        A future optimization would be to update this query only by new videos,
        or to redesign this as a handler that is only triggered when a new
        video is dropped.
        """

        # https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/youtube_v3.search.html
        response = self.client.search().list(
            part="id",
            channelId=channel_id,
            maxResults=max_results_per_query,
            order=order,
            type="video"
        ).execute()

        next_page_token = response.get("nextPageToken", None)
        video_ids = [
            item["id"]["videoId"] for item in response.get("items", [])
            if item["id"]["kind"] == "youtube#video"
        ]

        while True and len(video_ids) < max_results_total:
            response = self.client.search().list(
                part="id",
                channelId=channel_id,
                maxResults=max_results_per_query,
                order=order,
                type="video",
                pageToken=next_page_token
            ).execute()
            if "items" in response:
                video_ids.extend([
                    item["id"]["videoId"] for item in response.get("items", [])
                    if item["id"]["kind"] == "youtube#video"
                ])
            if "nextPageToken" in response:
                next_page_token = response["nextPageToken"]
            else:
                break

        return video_ids[:max_results_total]

    @manage_rate_limit_throttling
    def get_video_details_from_id(
        self, video_id: str, part_str: Optional[str] = "snippet,statistics"
    ) -> Dict:
        """Given a video ID, get the details about the video."""
        response = self.client.videos().list(
            part=part_str,
            id=video_id
        ).execute()
        return response


    def parse_video_response(self, video_response: Dict) -> Dict:
        """Given video response data from API request, parse the metadata and
        return in a flattened dictionary.
        
        NOTE: this could be a place where, if we wanted to do enrichment or
        other parsing, it could be done here. As a matter of principle I think
        it's better that this portion of a data pipeline should be purely
        extraction and that transformation should happen downstream.
        """
        metadata = video_response["items"][0]["snippet"]
        video_statistics = video_response["items"][0]["statistics"]
        video_statistics["viewCount"] = int(
            video_statistics.get("viewCount"), 0
        )
        video_statistics["likeCount"] = int(
            video_statistics.get("likeCount"), 0
        )
        video_statistics["favoriteCount"] = int(
            video_statistics.get("favoriteCount"), 0
        )
        video_statistics["commentCount"] = int(
            video_statistics.get("commentCount"), 0
        )
        return metadata, video_statistics


    def get_video_stats_for_channel_by_video(
        self,
        channel_id: Optional[str] = None,
        max_results_total: Optional[int] = 20,
        max_results_per_query: Optional[int] = 20,
        order: Optional[str] = "date"
    ) -> List[Dict]:
        """Gets statistics and metadata for each video in a channel, and
        returns as a list.
        """
        video_ids = self.get_video_ids_for_channel(
            channel_id=channel_id,
            max_results_total=max_results_total,
            max_results_per_query=max_results_per_query,
            order=order
        )

        video_info_list = []

        for video_id in video_ids:
            video_response = self.get_video_details_from_id(
                video_id=video_id
            )
            video_metadata, video_statistics = (
                self.parse_video_response(video_response)
            )

            # Extract relevant details
            video_info = {
                'video_id': video_id,
                "metadata": video_metadata,
                "statistics": video_statistics,
                **helper.METADATA_TO_HYDRATE
            }

            video_info_list.append(video_info)

        return video_info_list
