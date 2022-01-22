from django.conf import settings
import googleapiclient.discovery as discovery
import pytube
import os

from api import models, serializers

yt = discovery.build(
	"youtube",
	"v3",
	developerKey=settings.API_KEY
)

class Youtube:
	def __init__(self):
		self.api = discovery.build(
			"youtube",
			"v3",
			developerKey=settings.API_KEY
		)

	def validate_channel_id(self, channel_id):
		return True

	def validate_playlist_id(self, playlist_id):
		return True

	def format_playlists(self, playlists):
		"Format data to needed shape -> django model attributes."
		return [
			{
				"id": item["id"],
				"title": item["snippet"]["title"],
				"thumbnail": item["snippet"]["thumbnails"]["default"]["url"], 
				"description": item["snippet"]["description"],
				"channel": item["snippet"]["channelId"]
			} for item in playlists["items"]
		]

	def fetch_playlists(self, channel_id):
		assert self.validate_channel_id(channel_id)
		playlists = self.api.playlists().list(
			part="snippet,contentDetails",
			channelId=channel_id,
		).execute()
		
		# Re-format  
		playlists = self.format_playlists(playlists)

		return playlists
		
	def fetch_videos(self, playlist_id):
		assert self.validate_playlist_id(playlist_id)

		# Get the videos given a playlist id (just the needed data)
		playlist_items = self.api.playlistItems().list(
			part="snippet",
			playlistId=playlist_id,
			maxResults=1000		# HACK: Instead of pagination, put a high number
		).execute()

		videos = [
			{
				"id": item["snippet"]["resourceId"]["videoId"],
				"title": item["snippet"]["title"],
				"thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
				"description": item["snippet"]["description"],
				"channel_name": item["snippet"]["videoOwnerChannelTitle"]
			} for item in playlist_items["items"]
		]

		return videos

def get_online_videos_queue():
	"Return a serialized (JSON) queue of 'ONLINE' on synced playlists"
	qs = models.Video.objects.filter(state=models.Video.ONLINE, playlists__is_synced=True)
	qs_serializer = serializers.VideoSerializer(qs, many=True)
	return qs_serializer.data

def get_downloading_videos_queue():
	"Return a serialized (JSON) queue of 'DOWNLOADING'"
	qs = models.Video.objects.filter(state=models.Video.DOWNLOADING)
	qs_serializer = serializers.VideoSerializer(qs, many=True)
	return qs_serializer.data

def download_video(video_id):
	"Download the youtube video given its id"

	print(f"{video_id}: Downloading...")
	# try:
	# DOWNLOADING
	yt = pytube.YouTube(
		f'http://youtube.com/watch?v={video_id}',
		on_complete_callback=lambda *args: on_download_complete(video_id),
	)

	# Choose a low res
	low_res_stream = yt.streams.filter(
		progressive=True, 
		file_extension='mp4'
	).order_by(
		'resolution'
	).first()
	
	# HACK: update database before downloading.
	# TODO: This should be moved to a 'on_download_progress' function.
	video = models.Video.objects.get(id=video_id)
	video.state = models.Video.DOWNLOADING
	video.save()

	# Download to MEDIA_ROOT/video.id directory
	low_res_stream.download(output_path=settings.MEDIA_ROOT, filename=f"{video.id}.mp4")

	# except:
	# 	print("ERROR")

	return True

def on_download_complete(video_id):
	"Update the video instance in the database with new info"
	video = models.Video.objects.get(id=video_id)

	# SAVING THE NEW STATE
	video.state = models.Video.OFFLINE
	video.src = os.path.join(settings.MEDIA_URL, f"{video.id}.mp4")
	video.save()

	print(f"{video_id}: Done!")

	return True