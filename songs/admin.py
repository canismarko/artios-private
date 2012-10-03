from django.contrib import admin
from songs.models import *

admin.site.register(Song)
admin.site.register(SongStatus)
admin.site.register(SetList)
admin.site.register(SetListSong)
admin.site.register(Set)
