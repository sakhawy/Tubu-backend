from django.db import models

class Playlist(models.Model):
	id = models.CharField(max_length=100, primary_key=True)
	title = models.CharField(max_length=100)
	thumbnail = models.URLField(blank=True, null=True)
	description = models.TextField()
	username = models.CharField(max_length=30)
	is_synced = models.BooleanField(default=False)

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
	description = models.TextField()
	username = models.CharField(max_length=30)
	playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="videos")
	state = models.CharField(max_length=100, choices=STATE)

	def __str__(self):
		return self.title