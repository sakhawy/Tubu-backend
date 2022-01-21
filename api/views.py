from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from api import models, serializers
from utils.utils import Youtube

class PlaylistViewSet(viewsets.ModelViewSet):
	queryset = models.Playlist.objects.all()
	serializer_class = serializers.PlaylistSerializer

	@action(methods=["post"], detail=False)
	def fetch(self, request):
		# Fetch the playlists of a given channel id from youtube
		channel_id = request.data.get("channel_id", None)
		if channel_id:
			# HACK: Get or create the channel
			# TODO: Get from API
			models.Channel.objects.get_or_create(id=channel_id, name="HACK")

			# Talk to the API & save to DB
			playlists = Youtube().fetch_playlists(channel_id)

			for playlist in playlists:
				# Update playlist with custom fields
				playlist = {
					**playlist,
					**{
						
					}
				}
				playlist_serializer = serializers.PlaylistSerializer(data=playlist)
				if playlist_serializer.is_valid():
					playlist = playlist_serializer.save()
				else:
					# Already exists
					pass
			
			all_playlists = models.Playlist.objects.filter(channel_id=channel_id) 
			return Response(serializers.PlaylistSerializer(all_playlists, many=True).data, status=status.HTTP_200_OK)

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
