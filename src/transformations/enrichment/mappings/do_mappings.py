"""Map podcast information across different integrations."""
from transformations.enrichment.mappings import helper
from transformations.enrichment.mappings.map_channels import map_channels
from transformations.enrichment.mappings.map_episodes import map_episodes
from transformations.enrichment.mappings.sqlite_helper import (
    write_mapped_data_to_db
)

def main():
    """Enrich podcast information from Spotify with additional podcast
    information from YouTube, then write this shared information to DB."""

    """
    # get mappings
    mappings = map_channel_youtube_spotify_content(channel_name)

    # create unified Podcast object, with enriched data from both the YouTube
    # and the Spotify data.
    podcasts = [
        create_podcast_object(
            youtube_video=mapping["youtube_video"],
            spotify_episode=mapping["spotify_episode"]
        )
        for mapping in mappings
    ]

    # write to SQLite DB.
    for podcast in podcasts:
        write_mapped_data_to_db(podcast)
    """
    # TODO: figure out how to get channels to map. Could just get channels
    # from `channels` / `spotify_show` tables.
    CHANNELS = []
    for channel in CHANNELS:
        consolidated_channel_metadata = map_channels(channel)
        youtube_video_ids = (
            consolidated_channel_metadata["youtube_channel"]["episode_ids"]
        )
        spotify_episode_ids = (
            consolidated_channel_metadata["spotify_channel"]["episode_ids"]
        )

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
            mapped_episode = helper.create_mapped_episode_instance(
                episode
            )
            write_mapped_data_to_db(mapped_episode)

    print("Completed mapping podcasts across YouTube and Spotify integrations.") # noqa


if __name__ == "__main__":
    main()
