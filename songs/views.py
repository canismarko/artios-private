from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from artios_privatesite.songs.models import Song
from artios_privatesite.songs.forms import *

# List the songs in a table view
def list(request):
    song_list = Song.objects.all()
    return render_to_response('song_list.html',
                              locals(), 
                              RequestContext(request))

# Show a detailed view of each song
def detail(request, song_id, function="standard"):
    song = Song.objects.get(id=song_id)
    title = song.title + " - " + song.artist
    # Decide which details to show (eg lyrics, chords)
    if function == "standard":
        details_list = ["Key", song.key,
                        'Tempo', song.tempo,
                        'Status', song.status,
                        'Album', song.album,
                        'Order', song.order,
                        'Band Singer', song.band_singer,
                        'Band', song.band,
                        'Notes', song.notes
                        ]
    elif function == "lyrics":
        details_list = ['Lyrics', song.lyrics]
    elif function == "chords":
        details_list = ['Chords', song.chords]
    # Display the list
    return render_to_response('song_details.html',
                              locals(),
                              RequestContext(request))

# Edit the details of a song (excluding lyrics and notes which are in other views)
def edit(request, song_id=None, function="standard"):
    # First we figure out which form to use based on the value of 'function'
    if function == "standard":
        DynamicForm = SongEditForm
        redirect_uri_suffix = ""
    elif function == "lyrics":
        DynamicForm = SongLyricsForm
        redirect_uri_suffix = "lyrics/"
    elif function == "chords":
        DynamicForm = SongChordsForm
        redirect_uri_suffix = "chords/"
    else:
        return redirect('500.html')
    if request.method == 'POST': # Submitted a form
        if song_id > 0: # User asks to change a current song (ie edit)
            try:
                song = Song.objects.get(id=song_id)
            except Song.DoesNotExist: # Invalid song_id
                render('404.html')
            form = DynamicForm(request.POST, instance=song)
        else: # User did not submit a song_id (ie commiting a new song)
            form = DynamicForm(request.POST)
        if form.is_valid(): # Check for a valid form and submit
            instance = form.save()
            return redirect("/songs/" + str(instance.id) + "/" + redirect_uri_suffix)
    elif song_id > 0: # User submitted a song_id (needs populated edit form)
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist: # Invalid song_id
            # assert False
            return render_to_response('404.html',)
        title = song.title + " - " + song.artist
        form = DynamicForm(instance=song)
    elif song_id == None: # no song_id was given
        title = "New Song"
        form = DynamicForm()
    return render_to_response('song_details.html',
                              locals(),
                              RequestContext(request))
