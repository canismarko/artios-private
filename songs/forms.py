from django import forms
from artios_privatesite.songs.models import Song


class SongEditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'key', 'tempo', 'order', 'status', 'band_singer', 'band', 'notes']
