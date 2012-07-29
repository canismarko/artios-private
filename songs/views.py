import re
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from artios_privatesite.songs.models import Song
from artios_privatesite.songs.forms import *
from django.db.models import Q

# List the songs in a table view
def list(request, new_sort_field='none'):
    # TODO: Add ability to filter and search.
    #   search functions are already written
    #   below but might need modification.

    # Make sure the necessary variables exist
    try:
        request.session['sort_field']
        request.session['sort_order']
    except KeyError:
        request.session['sort_field'] = 'title'
        request.session['sort_order'] = 1
    # If the user asked to changed the order...
    if new_sort_field != 'none':
        # ...then set the session variables
        if request.session['sort_field'] == new_sort_field:
            request.session['sort_order'] = request.session['sort_order'] * -1
        else:
            request.session['sort_field'] = new_sort_field
            request.session['sort_order'] = 1
        return redirect('/songs/')
    # Construct the Model.order_by string
    if request.session['sort_order'] == -1:
        order_by_string = '-' + request.session['sort_field']
    else:
        order_by_string = request.session['sort_field']
    # Get the actual list of songs
    song_list = Song.objects.order_by(order_by_string)
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
@login_required
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

# Return a normalized search query
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

# Returns a query, to be used with Model.get()
def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
