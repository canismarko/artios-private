from django.contrib import admin
from artios_privatesite.songs.models import Song, SongStatus

admin.site.register(Song)
admin.site.register(SongStatus)
