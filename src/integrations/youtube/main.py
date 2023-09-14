"""Parent file encompassing extraction with the YouTube API.

Extracts data from YouTube API, for each channel, and then dumps into SQLite
tables.
"""
from integrations.youtube import constants, helper
from integrations.youtube.client import YoutubeClient
from integrations.youtube.sqlite_helper import write_youtube_data_to_db

def main():
    client = YoutubeClient()

    for channel_name, channel_id in constants.MAP_CHANNEL_HANDLE_TO_ID.items():
        channel_metadata = client.get_channel_metadata(channel_name)
        channel_id = channel_metadata["channelId"]
        video_metadata_list = (
            client.get_video_stats_for_channel_by_video(
                channel_id=channel_id
            )
        )
        channel = helper.create_channel_dataclass_instance(channel_metadata)
        videos = [
            helper.create_video_dataclass_instance(video_metadata)
            for video_metadata in video_metadata_list
        ]
        write_youtube_data_to_db(channel)
        for video in videos:
            write_youtube_data_to_db(video)


if __name__ == "__main__":
    main()
