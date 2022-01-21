from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from api import models, serializers

class PlaylistViewSet(viewsets.ModelViewSet):
	queryset = models.Playlist.objects.all()
	serializer_class = serializers.PlaylistSerializer

	@action(methods=["post"], detail=False)
	def fetch(self, request):
		# Fetch the playlists of a given channel id from youtube
		channel_id = request.data.get("channel_id", None)
		if channel_id:
			return Response("Hi")
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class VideoViewSet(viewsets.ModelViewSet):
	queryset = models.Video.objects.all()
	serializer_class = serializers.VideoSerializer

	@action(methods=["post"], detail=False)
	def fetch(self, request):
		# Fetch the videos of a given playlist from youtube
		playlist_id = request.data.get("playlist_id", None)
		if playlist_id:
			return Response("Hi")
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
