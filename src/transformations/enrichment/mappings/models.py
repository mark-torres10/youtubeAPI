from dataclasses import dataclass
from typing import List

from transformations.enrichment.constants import (
    MAPPED_CHANNEL_TABLE_NAME, MAPPED_EPISODES_TABLE_NAME
)


@dataclass
class MappedChannelIntegrationMetadata:
    """Class that contains integration-specific metadata for a given channel."""
    id: str
    name: str
    episode_ids: List[str]


@dataclass
class MappedChannel:
    """Class that contains key identifiers for a given channel, after
    consolidation across different sources.

    Contains a consolidated name and unique uuid, and then integration-specific
    information.
    """
    __table_name__ = MAPPED_CHANNEL_TABLE_NAME
    consolidated_name: str # PK
    youtube_channel: MappedChannelIntegrationMetadata
    spotify_channel: MappedChannelIntegrationMetadata
    last_updated_timestamp: str


@dataclass
class MappedEpisodeIntegrationMetadata:
    """Class that contains integration-specific metadata for a given episode."""
    id: str
    channel_id: str  # the integration's channel ID, not the MappedChannel ID
    name: str


@dataclass
class MappedEpisode:
    """Class that contains key identifiers for a given episode, after
    consolidation across different sources.

    Contains a consolidated name and unique uuid, and then integration-specific
    information.
    """
    __table_name__ = MAPPED_EPISODES_TABLE_NAME
    consolidated_name: str # PK
    mapped_channel_name: str  # FK, PK of MappedChannel
    consolidated_description: str
    youtube_episode: MappedEpisodeIntegrationMetadata
    spotify_episode: MappedEpisodeIntegrationMetadata
