from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from artios_privatesite.songs.models import Song

def list(request):
    song_list = Song.objects.all()
    return render_to_response('song_list.html',
                              locals(), 
                              RequestContext(request))

def add(request):
    pass

def detail(request, song_id):
    song = Song.objects.get(id=song_id)
    return render_to_response('song_details.html',
                              locals(),
                              RequestContext(request))

def edit(request, song_id):
    song = Song.objects.get(id=song_id)
    return render_to_response('song_modify.html',
                              locals(),
                              RequestContext(request))

def lyrics(request, song_id):
    song = Song.objects.get(id=song_id)
    return render_to_response('song_lyrics.html',
                              locals(),
                              RequestContext(request))

def chords(request, song_id):
    song = Song.objects.get(id=song_id)
    return render_to_response('song_lyrics.html',
                              locals(),
                              RequestContext(request))
