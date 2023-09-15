from dataclasses import dataclass
from typing import List


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
    id: str
    consolidated_name: str
    youtube_channel: MappedChannelIntegrationMetadata
    spotify_channel: MappedChannelIntegrationMetadata
    last_updated_timestamp: str


@dataclass
class MappedEpisodeIntegrationMetadata:
    """Class that contains integration-specific metadata for a given episode."""
    id: str
    channel_id: str # the integration's channel ID, not the MappedChannel ID
    name: str


@dataclass
class MappedEpisode:
    """Class that contains key identifiers for a given episode, after
    consolidation across different sources.
    
    Contains a consolidated name and unique uuid, and then integration-specific
    information.
    """
    id: str
    channel_id: str # id from MappedChannel
    consolidated_name: str
    consolidated_description: str
    youtube_episode: MappedEpisodeIntegrationMetadata
    spotify_episode: MappedEpisodeIntegrationMetadata
