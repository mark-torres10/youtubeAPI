"""Map podcast information across different integrations."""
from typing import List

from transformations.enrichment.mappings import helper
from transformations.enrichment.mappings.map_channels import map_channels
from transformations.enrichment.mappings.map_episodes import map_episodes
from transformations.enrichment.mappings.sqlite_helper import write_mapped_data_to_db
from lib.log.logger import Logger

logger = Logger(__name__)


def main() -> None:
    """Creates unified definitions of podcast channels and episodes across
    different integrations by mapping them together."""
    CHANNELS: List[str] = []

    logger.info("Starting to map podcasts across YouTube and Spotify integrations.")

    tables_to_sqlite_data_map = helper.get_map_tables_to_sqlite_data()
    youtube_channels_df = tables_to_sqlite_data_map["channels"]
    youtube_videos_df = tables_to_sqlite_data_map["youtube_videos"]
    spotify_shows_df = tables_to_sqlite_data_map["spotify_show"]
    spotify_episodes_df = tables_to_sqlite_data_map["spotify_episode"]

    mapped_channels = map_channels(
        youtube_channels_df=youtube_channels_df,
        spotify_shows_df=spotify_shows_df,
        youtube_videos_df=youtube_videos_df,
        spotify_episodes_df=spotify_episodes_df,
    )

    for mapped_channel in mapped_channels:
        youtube_video_ids = mapped_channel.youtube_episode.episode_ids
        spotify_episode_ids = mapped_channel.spotify_episode.episode_ids
        youtube_videos = helper.get_youtube_videos(youtube_video_ids)
        spotify_episodes = helper.get_spotify_episodes(spotify_episode_ids)
        mapped_episodes = map_episodes(
            youtube_videos=youtube_videos, spotify_episodes=spotify_episodes
        )
        write_mapped_data_to_db(mapped_channel)
        for episode in mapped_episodes:
            mapped_episode = helper.create_mapped_episode_instance(episode)
            write_mapped_data_to_db(mapped_episode)

    logger.info("Completed mapping podcasts across YouTube and Spotify integrations.")


if __name__ == "__main__":
    main()
