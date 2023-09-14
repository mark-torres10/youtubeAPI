"""Map podcast information across different integrations."""
from transformations.enrichment.helper import (
    create_podcast_object, write_podcast_object
)
from transformations.enrichment.mapping import (
    map_channel_youtube_spotify_content
)

def main():
    """Enrich podcast information from Spotify with additional podcast
    information from YouTube, then write this shared information to DB."""

    # TODO: need to unify these across YouTube + Spotify, but likely can
    # hardcode this as a map and just do a lookup.
    channel_name = ""

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
    for podcast in podcasts
        write_mapped_data_to_db(podcast)
    
    print(f"Completed writing {len(podcasts)} mappings to DB.")
    print("Enrichment complete.")

if __name__ == "__main__":
    main()
