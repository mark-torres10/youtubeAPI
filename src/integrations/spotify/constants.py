# list of endpoints: https://developer.spotify.com/blog/2020-03-20-introducing-podcasts-api

PODCAST_SHOW_ENDPOINT = "https://api.spotify.com/v1/shows/{id}?market={market}"
SPOTIFY_SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
PODCAST_SHOW_EPISODES_ENDPOINT = (
    "https://api.spotify.com/v1/shows/{id}/episodes"  # noqa
)

SPOTIFY_SHOW_NAME_TO_ID_MAP = {"Huberman Lab": "79CkJF3UJTHFV8Dse3Oy0P"}

# list of strings need to be transformed into comma-separated values.
SPOTIFY_LIST_STRING_FIELDS = [
    "available_markets",
    "copyrights",
    "episode_ids",
    "languages",
]
