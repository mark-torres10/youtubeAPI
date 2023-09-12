"""Parent file encompassing extraction with the YouTube API."""
from integrations.youtube.client import YoutubeClient
from integrations.youtube import helper

def main():
    # initialize client
    # get info about the latest videos for a given channel.
    # dump into PostgreSQL DB.
    client = YoutubeClient()

    for channel_handle, channel_id in helper.MAP_CHANNEL_HANDLE_TO_ID.items():
        video_id_to_info_map = (
            client.get_latest_video_stats_for_channel_by_video(
                handle=channel_handle, channel_id=channel_id
            )
        )

        # TODO: create Channel and Video instances and dump to their
        # SQL tables as necessary.
