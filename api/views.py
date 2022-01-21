from rest_framework import viewsets

from api import models, serializers

class PlaylistViewSet(viewsets.ModelViewSet):
	queryset = models.Playlist.objects.all()
	serializer_class = serializers.PlaylistSerializer

class VideoViewSet(viewsets.ModelViewSet):
	queryset = models.Video.objects.all()
	serializer_class = serializers.VideoSerializer
