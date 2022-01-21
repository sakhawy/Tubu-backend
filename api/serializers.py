from rest_framework import serializers

from api import models

class PlaylistSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Playlist
		fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Video
		fields = '__all__'

class ChannelSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Channel
		fields = '__all__'

	playlists = PlaylistSerializer(many=True, read_only=True)