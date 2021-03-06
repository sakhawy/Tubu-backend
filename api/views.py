from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from api import models, serializers
from utils.utils import Youtube

class PlaylistViewSet(viewsets.ModelViewSet):
	queryset = models.Playlist.objects.all()
	serializer_class = serializers.PlaylistSerializer

	# OVERRIDING this method to get the channel's playlists (GET requests)
	def get_queryset(self):
		channel_id = self.request.query_params.get('channel_id', None)
		queryset = models.Playlist.objects.all()
		if channel_id:
			queryset = queryset.filter(channel__id=channel_id)

		return queryset

	@action(methods=["post"], detail=False)
	def fetch(self, request):
		# Fetch the playlists of a given channel id from youtube
		channel_id = request.data.get("channel_id", None)
		if channel_id:
			# HACK: Get or create the channel
			# TODO: Get from API
			models.Channel.objects.get_or_create(id=channel_id, name=channel_id)

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
			
			all_playlists = models.Playlist.objects.filter(channel__id=channel_id) 
			return Response(serializers.PlaylistSerializer(all_playlists, many=True).data, status=status.HTTP_200_OK)

		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class VideoViewSet(viewsets.ModelViewSet):
	queryset = models.Video.objects.all()
	serializer_class = serializers.VideoSerializer

	# OVERRIDING this method to get the playlists' videos (GET requests)
	def get_queryset(self):
		playlist_id = self.request.query_params.get('playlist_id', None)
		queryset = models.Video.objects.all()
		if playlist_id:
			queryset = queryset.filter(playlists__id=playlist_id)

		return queryset

	@action(methods=["post"], detail=False)
	def fetch(self, request):
		# Fetch the videos of a given playlist from youtube
		playlist_id = request.data.get("playlist_id", None)
		if playlist_id:
			# Talk to the API & save to DB
			videos = Youtube().fetch_videos(playlist_id)

			for video in videos:
				# Update playlist with custom fields

				video = {
					**video,
					**{
						"playlists": [
							playlist_id
						]
					}
				}

				video_serializer = serializers.VideoSerializer(data=video)
				if video_serializer.is_valid():
					video = video_serializer.save()
					
					# Add the playlist
					playlist = models.Playlist.objects.get(id=playlist_id)
					video.playlists.add(playlist)
					video.save()

				else:
					# Already exists
					print(video_serializer.errors)

			all_videos = models.Video.objects.filter(playlists__id=playlist_id) 
			return Response(serializers.VideoSerializer(all_videos, many=True).data, status=status.HTTP_200_OK)

		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
