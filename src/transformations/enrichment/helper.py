from typing import Dict

import pandas as pd

from db.sql.constants import TABLE_NAME_TO_KEYS_MAP
from db.sql.helper import get_all_table_results_as_df
from transformations.enrichment.models import PodcastEpisode

def get_map_tables_to_sqlite_data() -> Dict[str, pd.DataFrame]:
    """Get all the current data in the SQLite DB."""
    return {
        table_name: get_all_table_results_as_df(table_name)
        for table_name in TABLE_NAME_TO_KEYS_MAP.keys()
    }


def create_podcast_object(
    youtube_video: Dict, spotify_episode: Dict
) -> PodcastEpisode:
    pass
