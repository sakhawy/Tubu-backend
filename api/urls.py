from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'videos', views.VideoViewSet)
router.register(r'channels', views.ChannelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]