from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from artios_privatesite.songs.models import Song
from artios_privatesite.songs.forms import SongEditForm

# List the songs in a table view
def list(request):
    song_list = Song.objects.all()
    return render_to_response('song_list.html',
                              locals(), 
                              RequestContext(request))

# Add a new song
def add(request):
    pass

# Show a detailed view of each song
def detail(request, song_id):
    song = Song.objects.get(id=song_id)
    return render_to_response('song_details.html',
                              locals(),
                              RequestContext(request))

# Edit the details of a song (excluding lyrics and notes which are in other views)
def edit(request, song_id):
    song = Song.objects.get(id=song_id)
    form = SongEditForm(instance=song)
    return render_to_response('song_details.html',
                              locals(),
                              RequestContext(request))

# Show the lyrics of a song
def lyrics(request, song_id):
    song = Song.objects.get(id=song_id)
    return render_to_response('song_lyrics.html',
                              locals(),
                              RequestContext(request))

# Show the chord changes to a song
def chords(request, song_id):
    song = Song.objects.get(id=song_id)
    return render_to_response('song_lyrics.html',
                              locals(),
                              RequestContext(request))
