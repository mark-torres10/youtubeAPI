TABLE_NAME_TO_SCHEMA_MAP = {
    "youtube_channels": """
        channel_id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        channel_title TEXT,
        publish_time TEXT,
        published_at TEXT,
        synctimestamp TEXT
    """,
    "youtube_videos": """
        video_id TEXT PRIMARY KEY,
        video_title TEXT,
        channel_id TEXT,
        channel_title TEXT,
        category_id TEXT,
        default_audio_language TEXT,
        default_language TEXT,
        description TEXT,
        live_broadcast_content TEXT,
        published_at TEXT,
        tags TEXT,
        view_count INTEGER,
        like_count INTEGER,
        favorite_count INTEGER,
        comment_count INTEGER,
        synctimestamp TEXT
    """,
    "spotify_show": """
        id TEXT PRIMARY KEY,
        available_markets TEXT,  -- Comma-separated list of markets
        copyrights TEXT,  -- Comma-separated list of copyrights
        description TEXT,
        explicit INTEGER,  -- Store as 0 for False, 1 for True
        href TEXT,
        html_description TEXT,
        is_externally_hosted INTEGER,  -- Store as 0 for False, 1 for True
        languages TEXT,  -- Comma-separated list of languages
        media_type TEXT,
        name TEXT,
        publisher TEXT,
        type TEXT,
        uri TEXT,
        total_episodes INTEGER,
        episode_ids TEXT,  -- Comma-separated list of episode IDs
        synctimestamp TEXT
    """,
    "spotify_episode": """
        id TEXT PRIMARY KEY,
        show_id TEXT,  -- Foreign key to link episodes to shows (assuming a shows table)
        show_name TEXT,
        audio_preview_url TEXT,
        description TEXT,
        html_description TEXT,
        duration_ms INTEGER,
        explicit INTEGER,  -- Store as 0 for False, 1 for True (SQLite doesn't have a BOOLEAN type)
        href TEXT,
        is_externally_hosted INTEGER,  -- Store as 0 for False, 1 for True
        is_playable INTEGER,  -- Store as 0 for False, 1 for True
        languages TEXT,  -- Comma-separated list of languages
        name TEXT,
        release_date TEXT,
        release_date_precision TEXT,
        type TEXT,
        uri TEXT,
        synctimestamp TEXT
    """,  # noqa
    "mapped_channels": """
        consolidated_name TEXT PRIMARY KEY,
        youtube_channel_id TEXT,
        youtube_channel_name TEXT,
        youtube_episode_ids TEXT,  -- Comma-separated list of episode IDs
        spotify_show_id TEXT,
        spotify_show_name TEXT,
        spotify_episode_ids TEXT,  -- Comma-separated list of episode IDs
        last_updated_timestamp TEXT
    """,
    "mapped_episodes": """
        consolidated_name TEXT PRIMARY KEY,
        mapped_channel_name TEXT,  -- Foreign key to link episodes to channels (assuming a channels table)
        consolidated_description TEXT,
        youtube_episode_id TEXT,
        youtube_episode_channel_id TEXT,
        youtube_episode_name TEXT,
        spotify_episode_id TEXT,
        spotify_episode_show_id TEXT,
        spotify_episode_show_name TEXT,
        last_updated_timestamp TEXT
    """
}


TABLE_NAME_TO_KEYS_MAP = {
    "channels": {"primary": ["channel_id"], "foreign": None},
    "videos": {"primary": ["video_id"], "foreign": ["channel_id"]},
    "spotify_show": {"primary": ["id"], "foreign": ["episode_ids"]},
    "spotify_episode": {"primary": ["id"], "foreign": ["show_id"]},
}
