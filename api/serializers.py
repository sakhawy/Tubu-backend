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
