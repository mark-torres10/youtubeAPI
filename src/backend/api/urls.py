from django.urls import path
from . import views

urlpatterns = [
    path('channels/', views.MappedChannelList.as_view(), name='channel-list'),
    path('episodes/', views.MappedEpisodeList.as_view(), name='episode-list'),
]
