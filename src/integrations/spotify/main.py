"""Parent file encompassing extraction with the Spotify API.

Setting up Spotify API access: https://developer.spotify.com/dashboard
"""
from integrations.spotify import helper
from integrations.spotify.client import SpotifyClient
from integrations.spotify.constants import SPOTIFY_SHOW_NAME_TO_ID_MAP
from integrations.spotify.sqlite_helper import write_spotify_data_to_db

def main():
    client = SpotifyClient()
    for _, show_id in SPOTIFY_SHOW_NAME_TO_ID_MAP.items():
        show_metadata = client.get_podcast_show_metadata(show_id=show_id)
        episode_metadata_list = client.get_episode_details_for_podcast_show(
            show_id=show_id
        )
        spotify_show = helper.create_spotify_show_instance(show_metadata)
        spotify_episodes = [
            helper.create_spotify_episode_instance(episode_metadata)
            for episode_metadata in episode_metadata_list
        ]
        write_spotify_data_to_db(spotify_show)
        for episode in spotify_episodes:
            write_spotify_data_to_db(episode)
