"""Access to YouTube API.

Auth details: https://developers.google.com/youtube/v3/quickstart/python
Helpful start resource: https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
API start docs: https://developers.google.com/youtube/v3/docs/?apix=true#Channels
Full API docs: https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/
"""  # noqa
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple, Union

from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

from db.redis.redis_caching import cache_data, get_cached_data
from lib.sync_enrichment import METADATA_TO_HYDRATE
from lib.log.logger import Logger

load_dotenv(Path("../../../.env"))

logger = Logger(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def manage_rate_limit_throttling(func: Callable) -> Callable:
    def wrapper(*args: Tuple, **kwargs: Dict) -> Any:
        try:
            result = func(*args, **kwargs)
            return result
        except HttpError as e:
            if e.resp.status == 429:
                # TODO: investigate rate limits to figure out backoff strategy
                # print("Rate limit exceeded. Waiting and retrying...")
                # time.sleep(60)  # Sleep for 60 seconds (adjust as needed)
                return wrapper(*args, **kwargs)  # Retry the function
            else:
                # Handle other HTTP errors here, e.g., log or raise an exception
                logger.error(f"HTTP error: {e}")
                return {"error": f"HTTP error: {e}"}

    return wrapper


class YoutubeClient:
    def __init__(self) -> None:
        self.client: Resource = build(
            "youtube", "v3", developerKey=YOUTUBE_API_KEY
        )

    # https://developers.google.com/youtube/v3/guides/working_with_channel_ids
    def get_channel_id_from_handle(self, handle: str) -> str:
        """Gets channel ID from a handle.

        NOTE: need to get this implementing, but API docs seem to be misleading
        """
        cached_data = get_cached_data(
            function_name="get_channel_id_from_handle", params={"handle": handle}
        )
        if cached_data and len(cached_data) > 0:
            return cached_data
        response = self.client.channels().list(part="id", forUsername=handle).execute()

        res = response["etag"]
        cache_data(
            function_name="get_channel_id_from_handle",
            params={"handle": handle},
            data=res,
        )
        return res

    # # https://developers.google.com/youtube/v3/guides/working_with_channel_ids
    @manage_rate_limit_throttling
    def get_channel_metadata(self, channel_name: str) -> Dict:
        """Retrieve channel information from the channel name.

        NOTE: this approach returns multiple possibilities. Ideally would use
        the channel tags instead. For a first pass, just returning the
        first result, since this will give us the most likely result.
        """
        params = {"channel_name": channel_name}
        cached_data = get_cached_data(
            function_name="get_channel_metadata", params=params
        )
        if cached_data and len(cached_data) > 0:
            return cached_data

        response = (
            self.client.search()
            .list(part="snippet", type="channel", q=channel_name)
            .execute()
        )
        metadata = response["items"][0]["snippet"]

        res = {**metadata, **METADATA_TO_HYDRATE}
        cache_data(function_name="get_channel_metadata", params=params, data=res)
        return res

    @manage_rate_limit_throttling
    def get_video_ids_for_channel(
        self,
        channel_id: str,
        max_results_total: int = 20,
        max_results_per_query: int = 20,
        order: str = "date",
    ) -> List[str]:
        """Get all the videos that are available for a given channel.

        TODO: for a data pipeline, we would only get the videos that are new.
        A future optimization would be to update this query only by new videos,
        or to redesign this as a handler that is only triggered when a new
        video is dropped.
        # https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/youtube_v3.search.html

        TODO: need to think of a better caching strategy since pagination
        tokens expire (it seems?)
        """  # noqa
        params = {
            "channel_id": channel_id,
            "max_results_total": max_results_total,
            "max_results_per_query": max_results_per_query,
            "order": order,
        }
        cached_data = get_cached_data(
            function_name="get_video_ids_for_channel", params=params
        )
        if cached_data and len(cached_data) > 0:
            return cached_data
        response = (
            self.client.search()
            .list(
                part="id",
                channelId=channel_id,
                maxResults=max_results_per_query,
                order=order,
                type="video",
            )
            .execute()
        )

        next_page_token = response.get("nextPageToken", None)
        video_ids = [
            item["id"]["videoId"]
            for item in response.get("items", [])
            if item["id"]["kind"] == "youtube#video"
        ]

        while True and len(video_ids) < max_results_total:
            pagination_params = {
                "part": "id",
                "channelId": channel_id,
                "maxResults": max_results_per_query,
                "order": order,
                "type": "video",
                "pageToken": next_page_token,
            }
            cached_data = get_cached_data(
                function_name="get_channel_metadata", params=pagination_params
            )
            cached_data = None
            response = (
                cached_data
                if cached_data and len(cached_data) > 0
                else self.client.search().list(**pagination_params).execute()
            )
            cache_data(
                function_name="get_channel_metadata",
                params=pagination_params,
                data=response,
            )

            if "items" in response:
                video_ids.extend(
                    [
                        item["id"]["videoId"]
                        for item in response.get("items", [])
                        if item["id"]["kind"] == "youtube#video"
                    ]
                )
            if "nextPageToken" in response:
                next_page_token = response["nextPageToken"]
            else:
                break

        return video_ids[:max_results_total]

    @manage_rate_limit_throttling
    def get_video_details_from_id(
        self, video_id: str, part_str: str = "snippet,statistics"
    ) -> Dict:
        """Given a video ID, get the details about the video."""
        params = {"part": part_str, "id": video_id}
        cached_data = get_cached_data(
            function_name="get_video_details_from_id", params=params
        )
        if cached_data and len(cached_data) > 0:
            return cached_data

        response = self.client.videos().list(**params).execute()
        cache_data(
            function_name="get_video_details_from_id", params=params, data=response
        )
        return response

    def parse_video_response(
        self, video_response: Dict
    ) -> Tuple[Dict[str, str], Dict[str, Union[str, int]]]:
        """Given video response data from API request, parse the metadata and
        return in a flattened dictionary.

        NOTE: this could be a place where, if we wanted to do enrichment or
        other parsing, it could be done here. As a matter of principle I think
        it's better that this portion of a data pipeline should be purely
        extraction and that transformation should happen downstream.
        """
        metadata: Dict[str, str] = video_response["items"][0]["snippet"]
        video_statistics: Dict[str, Union[str, int]]  = (
            video_response["items"][0]["statistics"]
        )
        video_statistics["viewCount"] = int(video_statistics.get("viewCount"), 0) # type: ignore
        video_statistics["likeCount"] = int(video_statistics.get("likeCount"), 0) # type: ignore
        video_statistics["favoriteCount"] = int(
            video_statistics.get("favoriteCount"), 0 # type: ignore
        )
        video_statistics["commentCount"] = int(video_statistics.get("commentCount"), 0) # type: ignore
        return metadata, video_statistics

    def get_video_stats_for_channel_by_video(
        self,
        channel_id: str,
        max_results_total: int = 20,
        max_results_per_query: int = 20,
        order: str = "date",
    ) -> List[Dict]:
        """Gets statistics and metadata for each video in a channel, and
        returns as a list.
        """
        video_ids = self.get_video_ids_for_channel(
            channel_id=channel_id,
            max_results_total=max_results_total,
            max_results_per_query=max_results_per_query,
            order=order,
        )

        video_info_list = []

        for video_id in video_ids:
            video_response = self.get_video_details_from_id(video_id=video_id)
            if video_response["pageInfo"]["totalResults"] == 0:
                continue

            video_metadata, video_statistics = self.parse_video_response(video_response)

            video_info = {
                "video_id": video_id,
                "metadata": video_metadata,
                "statistics": video_statistics,
                **METADATA_TO_HYDRATE,
            }

            video_info_list.append(video_info)

        return video_info_list
