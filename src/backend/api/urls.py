from django.urls import path
from . import views

urlpatterns = [
    path('channels/', views.ChannelList.as_view(), name='channel-list'),
    path('episodes/', views.EpisodeList.as_view(), name='episode-list'),
]
