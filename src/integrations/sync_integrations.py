"""Parent file to re-sync data from each integration."""
from integrations.spotify import main as spotify_sync
from integrations.youtube import main as youtube_sync


def main() -> None:
    youtube_sync.main()
    spotify_sync.main()
