from django.conf import settings
import googleapiclient.discovery as discovery

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
			playlistId=playlist_id
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
