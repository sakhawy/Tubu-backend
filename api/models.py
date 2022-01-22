from django.db import models

class Channel(models.Model):
	id = models.CharField(max_length=100, primary_key=True)
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.id

class Playlist(models.Model):
	id = models.CharField(max_length=100, primary_key=True)
	title = models.CharField(max_length=100)
	thumbnail = models.URLField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	is_synced = models.BooleanField(default=False)
	channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="playlists")

	def __str__(self):
		return self.title

class Video(models.Model):
	ONLINE = "ONLINE"
	DOWNLOADING = "DOWNLOADING"
	OFFLINE = "OFFLINE"
	DELETED = "DELETED"
	STATE = [
		(ONLINE, "Online"),
		(DOWNLOADING, "Downloading"),
		(OFFLINE, "Offline"),
		(DELETED, "Deleted"),
	]

	id = models.CharField(max_length=100, primary_key=True)
	title = models.CharField(max_length=100)
	thumbnail = models.URLField()
	src = models.URLField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	channel_name = models.CharField(max_length=100)
	playlists = models.ManyToManyField(Playlist, blank=True, related_name="videos")
	state = models.CharField(max_length=100, choices=STATE, default=ONLINE)

	def __str__(self):
		return self.title