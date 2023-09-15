"""SQLite helper utilities for writing mapped data."""
from typing import Union

from transformations.enrichment.mappings.models import (
    MappedChannel, MappedEpisode
)

def write_mapped_data_to_db(
    instance: Union[MappedChannel, MappedEpisode]
) -> None:
    pass
