from rest_framework import serializers
from .models import MappedChannelIntegrationMetadata, MappedChannel, MappedEpisodeIntegrationMetadata, MappedEpisode

class MappedChannelIntegrationMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappedChannelIntegrationMetadata
        fields = '__all__'

class MappedChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappedChannel
        fields = '__all__'

class MappedEpisodeIntegrationMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappedEpisodeIntegrationMetadata
        fields = '__all__'

class MappedEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappedEpisode
        fields = '__all__'
