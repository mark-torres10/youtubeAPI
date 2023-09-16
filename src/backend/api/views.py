from rest_framework import generics
from .models import Channel, Episode
from .serializers import ChannelSerializer, EpisodeSerializer

class ChannelList(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class EpisodeList(generics.ListCreateAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
