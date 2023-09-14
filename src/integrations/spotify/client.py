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

from integrations.spotify import constants

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

    def get_id_for_podcast_show(self, show_name: str) -> str:
        """Given a particular podcast show name, get the corresponding ID."""
        params = {
            'q': show_name,
            'type': 'show'
        }
        response = requests.get(
            constants.PODCAST_MULTIPLE_SHOWS_ENDPOINT,
            headers=self.headers,
            params=params
        )
        show_data = response.json()
        if 'shows' in show_data and show_data['shows']['items']:
            return show_data['shows']['items'][0]['id']
        else:
            return ""

    def get_podcast_show_metadata(self, show_id: str) -> Dict:
        """Get the details about a given show on Spotify."""
        endpoint = constants.PODCAST_SHOW_ENDPOINT.format(id=show_id)
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

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
            'limit': max_results
        }
        endpoint = constants.PODCAST_SHOW_EPISODES_ENDPOINT.format(id=show_id)
        episodes = []
        while endpoint:
            response = requests.get(endpoint, headers=headers, params=params)
            episode_data = response.json()
            episodes.extend(episode_data['items'])
            endpoint = episode_data['next']
        return episodes


if __name__ == "__main__":
    client = SpotifyClient()
    breakpoint()
