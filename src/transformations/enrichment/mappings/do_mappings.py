"""Map podcast information across different integrations."""
from typing import List

from transformations.enrichment.mappings import helper
from transformations.enrichment.mappings.map_channels import map_channels
from transformations.enrichment.mappings.map_episodes import map_episodes
from transformations.enrichment.mappings.sqlite_helper import write_mapped_data_to_db
from lib.log.logger import Logger

logger = Logger()

def main() -> None:
    """Creates unified definitions of podcast channels and episodes across
    different integrations by mapping them together."""
    CHANNELS: List[str] = []
    for channel in CHANNELS:
        consolidated_channel_metadata = map_channels(channel)
        youtube_video_ids = consolidated_channel_metadata["youtube_channel"][
            "episode_ids"
        ]
        spotify_episode_ids = consolidated_channel_metadata["spotify_channel"][
            "episode_ids"
        ]

        youtube_videos = helper.get_youtube_videos(youtube_video_ids)
        spotify_episodes = helper.get_spotify_episodes(spotify_episode_ids)

        mapped_episodes = map_episodes(
            youtube_videos=youtube_videos, spotify_episodes=spotify_episodes
        )

        mapped_channel = helper.create_mapped_channel_instance(
            consolidated_channel_metadata
        )
        write_mapped_data_to_db(mapped_channel)
        for episode in mapped_episodes:
            mapped_episode = helper.create_mapped_episode_instance(episode)
            write_mapped_data_to_db(mapped_episode)

    logger.info(
        "Completed mapping podcasts across YouTube and Spotify integrations."
    )


if __name__ == "__main__":
    main()
