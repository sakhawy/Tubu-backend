from django.db import models

class Playlist(models.Model):
	id = models.CharField(max_length=100, primary_key=True)
	title = models.CharField(max_length=100)
	thumbnail = models.URLField(blank=True, null=True)
	description = models.TextField()
	username = models.CharField(max_length=30)
	is_synced = models.BooleanField(default=False)

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
	description = models.TextField()
	username = models.CharField(max_length=30)
	playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="videos")
	state = models.CharField(choices=STATE)