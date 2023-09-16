from rest_framework import generics
from .models import MappedChannel, MappedEpisode
from .serializers import MappedChannelSerializer, MappedEpisodeSerializer

class MappedChannelList(generics.ListAPIView):
    queryset = MappedChannel.objects.all()
    serializer_class = MappedChannelSerializer

class MappedEpisodeList(generics.ListAPIView):
    queryset = MappedEpisode.objects.all()
    serializer_class = MappedEpisodeSerializer
