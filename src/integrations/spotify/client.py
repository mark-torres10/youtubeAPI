"""Access to Spotify API.

Python helper package details: https://spotipy.readthedocs.io/en/2.22.1/
Spotify web API details: https://developer.spotify.com/documentation/web-api
Getting started: https://developer.spotify.com/documentation/web-api/tutorials/getting-started
Details on accessing a given Spotify podcast: https://developer.spotify.com/documentation/web-api/reference/get-a-show
Details on accessing Spotify podcast episodes: https://developer.spotify.com/documentation/web-api/reference/get-a-shows-episodes

"""
import base64
from dotenv import load_dotenv
import os
from pathlib import Path
import requests
from typing import Dict, List, Optional

from db.redis.redis_caching import cache_data, get_cached_data
from integrations.spotify import constants
from lib.sync_enrichment import METADATA_TO_HYDRATE

load_dotenv(Path("../../../.env"))

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode() # noqa
token_url = 'https://accounts.spotify.com/api/token'
token_data = {
    'grant_type': 'client_credentials'
}
token_headers = {
    'Authorization': f'Basic {auth_header}'
}
response = requests.post(token_url, data=token_data, headers=token_headers)
access_token = response.json()['access_token']


class SpotifyClient:
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    # TODO: need to explore this endpoint more. In the meantime, OK to
    # hardcode an ID by looking at the Spotify console.
    def get_id_for_podcast_show(self, show_name: str) -> str:
        """Given a particular podcast show name, get the corresponding ID."""
        params = {
            'q': show_name,
            'type': 'show'
        }
        response = requests.get(
            constants.SPOTIFY_SEARCH_ENDPOINT,
            headers=self.headers,
            params=params
        )
        show_data = response.json()
        if 'shows' in show_data:
            if show_data["shows"]["total"] == 0:
                print(
                    f"No Spotify show found with show_name={show_name}"
                ) # TODO: should be logger
                return ""
            else:
                # TODO: likely need a better way to guarantee the results that
                # we want, but as a first pass this should be OK.
                return show_data['shows']['items'][0]['id']
        else:
            return ""


    def get_podcast_show_metadata(
        self,
        show_name: Optional[str] = None,
        show_id: Optional[str] = None
    ) -> Dict:
        if show_name and not show_id:
            show_id = self.get_id_for_podcast_show(show_name=show_name)
        """Get the details about a given show on Spotify."""
        endpoint = constants.PODCAST_SHOW_ENDPOINT.format(
            id=show_id, market="US"
        )
        params = {"show_id": show_id}

        cached_data = get_cached_data(
            function_name="get_podcast_show_metadata",
            params=params
        )
        if cached_data:
            return cached_data

        response = requests.get(endpoint, headers=self.headers)
        res = {
            **response.json(),
            **METADATA_TO_HYDRATE
        }
        if not cached_data:
            cache_data(
                function_name="get_podcast_show_metadata", params=params, data=res
            )
        return res


    def get_episode_details_for_podcast_show(
        self, show_id: str, max_results: Optional[int] = 20) -> List[Dict]:
        """Get the details of each episode in a given podcast show.
        
        Paginates through results to get the details for each episode,
        up to the `max_results` argument given.
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        params = {
            "market": "US",
            "limit": max_results
        }
        endpoint = constants.PODCAST_SHOW_EPISODES_ENDPOINT.format(id=show_id)
        episodes = []
        while endpoint:
            cached_data = get_cached_data(
                function_name="get_episode_details_for_podcast_show",
                params={
                    "endpoint": endpoint,
                    "params": params
                }
            )
            if cached_data:
                return cached_data
            response = requests.get(endpoint, headers=headers, params=params)
            episode_data = response.json()
            episodes.extend(
                {
                    **episode_data['items'],
                    **METADATA_TO_HYDRATE
                }
            )
            endpoint = episode_data['next']
            if not cached_data:
                cache_data(
                    function_name="get_episode_details_for_podcast_show",
                    params={
                        "endpoint": endpoint,
                        "params": params
                    },
                    data=episode_data
                )

        return episodes


if __name__ == "__main__":
    client = SpotifyClient()
    show_metadata = client.get_podcast_show_metadata(
        show_id="79CkJF3UJTHFV8Dse3Oy0P"
    )
    shows = client.get_episode_details_for_podcast_show(
        show_id="79CkJF3UJTHFV8Dse3Oy0P"
    )
    breakpoint()
