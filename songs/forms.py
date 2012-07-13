from django import forms
from artios_privatesite.songs.models import Song

# For editing the main details of a song
class SongEditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'key', 'tempo', 'order', 'status', 'band_singer', 'band', 'notes']

class SongLyricsForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['lyrics']

class SongChordsForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['chords']
