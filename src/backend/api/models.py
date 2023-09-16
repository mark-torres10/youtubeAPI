from django.db import models

from django.db import models

class MappedChannelIntegrationMetadata(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    # many-to-many relationship
    episode_ids = models.ManyToManyField('MappedEpisode', related_name='mapped_channels')

class MappedChannel(models.Model):
    consolidated_name = models.CharField(max_length=255, primary_key=True)
    youtube_channel = models.OneToOneField(MappedChannelIntegrationMetadata, on_delete=models.CASCADE, related_name='youtube_channel_for')
    spotify_channel = models.OneToOneField(MappedChannelIntegrationMetadata, on_delete=models.CASCADE, related_name='spotify_channel_for')
    last_updated_timestamp = models.DateTimeField()

class MappedEpisodeIntegrationMetadata(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    channel_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

class MappedEpisode(models.Model):
    consolidated_name = models.CharField(max_length=255, primary_key=True)
    mapped_channel_name = models.ForeignKey(MappedChannel, on_delete=models.CASCADE, related_name='mapped_episodes')
    consolidated_description = models.TextField()
    youtube_episode = models.OneToOneField(MappedEpisodeIntegrationMetadata, on_delete=models.CASCADE, related_name='youtube_episode_for')
    spotify_episode = models.OneToOneField(MappedEpisodeIntegrationMetadata, on_delete=models.CASCADE, related_name='spotify_episode_for')
