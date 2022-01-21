from django.contrib import admin

from api import models

class PlaylistAdmin(admin.ModelAdmin):
	list_diplay = ["__str__"]

class VideoAdmin(admin.ModelAdmin):
	list_diplay = ["__str__"]

class ChannelAdmin(admin.ModelAdmin):
	list_diplay = ["__str__"]

admin.site.register(models.Playlist, PlaylistAdmin)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.Channel, ChannelAdmin)