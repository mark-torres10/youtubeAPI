from datetime import datetime

YOUTUBE_CHANNEL_NAME = "Andrew Huberman"
YOUTUBE_CHANNEL_HANDLE = "hubermanlab"
YOUTUBE_CHANNEL_ID = "UC2D2CMWXMOVWx7giW1n3LIg"  # YouTube ID of Huberman podcast
SPOTIFY_CHANNEL_ID = ""  # Spotify ID of Huberman podcast
SQLITE_ENGINE = "sqlite:///youtube_data.db"
CURRENT_SYNCTIMESTAMP = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
