import re
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from artios_privatesite.songs.models import *
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

# Return a list of all the set-lists for the user to see
def setlists(request):
    '''
    View that displays all the set lists and allows the user to pick one
    '''
    set_lists = SetList.objects.all()
    return render_to_response('setlist_list.html',
                              locals(),
                              RequestContext(request))

@login_required
def setlist_edit(request, setlist_id=-1):
    '''
    A view which allows the user to edit a current setlist
    or add a new setlist. It also creates at least one set
    within a new setlist in order to avoid errors down
    the road.
    '''
    if request.method == 'POST': # Form is submitted...
        try:
            setlist = SetList.objects.get(id=setlist_id)
            form = SetListForm(request.POST, instance=setlist)
        except SetList.DoesNotExist:
            form = SetListForm(request.POST)
        if form.is_valid():
            setlist = form.save()
            if setlist_id == -1:
                # A new setlist needs at least one set or else errors occur in later views functions.
                set = Set(set_list=setlist, set_number=0)
                set.save()
            return redirect('/songs/setlists/')
    else: # form for editing...
        try:
            setlist = SetList.objects.get(id=setlist_id)
            setlist_form = SetListForm(instance=setlist)
        except SetList.DoesNotExist:
            setlist_form = SetListForm()
    return render_to_response('setlist_form.html',
                              locals(),
                              RequestContext(request))  

def setlist_detail(request, setlist_id):
    '''
    View that shows the details of a given set list
    '''
    # Get the set list and organize the sets into variable song_list
    setlist = SetList.objects.get(id=setlist_id)
    song_list = []
    sets = Set.objects.filter(set_list__id=setlist_id).order_by('set_number')
    for show_set in sets:
        if show_set.set_number == 0:
            unassigned_set = show_set
        else:
            songs = SetListSong.objects.filter(set__id=show_set.id).order_by('order')
            song_list.append(show_set.set_number)
            song_list.append(songs)
    if unassigned_set:
        songs = SetListSong.objects.filter(set__id=unassigned_set.id).order_by('order')
        song_list.append(unassigned_set.set_number)
        song_list.append(songs)
    # render the template
    return render_to_response('setlist_detail.html',
                              locals(),
                              RequestContext(request))

# allows the user to add or remove songs from a setlist pool
@login_required
def setlist_addremove(request, setlist_id):
    setlist = SetList.objects.get(id=setlist_id)
    unassigned_set = Set.objects.get(set_list__id=setlist_id, set_number=0)
    # The user has posted some data that needs to be processed
    if request.method == "POST":
        # First check for additions
        for request_song in request.POST:
            # For each checkbox, first make sure it's actually a song checkbox
            if request_song.rfind(u'song') == 0:
                song_number = str(request_song.strip('song'))
                song = Song.objects.get(id=song_number)
                try: # If the entry already exists, then nothing left to do
                    SetListSong.objects.get(song__id=song_number, set__set_list__id=setlist_id)
                except: # User added a new song to this set list
                    new_song = SetListSong(song=song, set=unassigned_set, order=0)
                    new_song.save()
        # Now test for removals
        set_list_songs = SetListSong.objects.filter(set__set_list__id=setlist_id)
        for set_list_song in set_list_songs:
            song_found = False
            for request_song in request.POST:
                try:
                    if int(request_song.strip('song')) == set_list_song.song.id:
                        song_found = True
                except ValueError:
                    pass
            if not song_found:
                set_list_song.delete()
        return redirect('/songs/setlists/' + str(setlist_id) + '/')
    # The user needs a blank form
    else:
        songs = Song.objects.order_by('title')
        song_list = []
        # This for loop makes a new list with the added ['checked'] item
        for song in songs:
            song_detail = {}
            try:
                SetListSong.objects.get(song__id=song.id, set__set_list__id=setlist_id)
                song_detail['checked'] = 'checked'
            except:
                song_detail['checked'] = ''
            song_detail['id'] = song.id
            song_detail['title'] = song.title
            song_detail['artist'] = song.artist
            song_detail['status'] = song.status.display
            song_list.append(song_detail)
    function = 'addremove'
    return render_to_response('setlist_detail.html',
                              locals(),
                              RequestContext(request))

# Allows the user to arrange the songs into sets
@login_required
def setlist_arrange(request, setlist_id):
    setlist = SetList.objects.get(id=setlist_id)
    sets = Set.objects.filter(set_list__id=setlist_id).order_by('set_number')
    if request.method == 'POST':
        for request_item in request.POST:
            # Modify the orders
            if request_item.find('txtOrder') > -1:
                setlistsong_id = int(request_item.strip('txtOrder'))
                setlistsong = SetListSong.objects.get(id=setlistsong_id)
                setlistsong.order = request.POST[request_item]
                setlistsong.save()
            # Modify the set relationships
            if request_item.find('slctSet') > -1:
                setlistsong_id = int(request_item.strip('slctSet'))
                setlistsong = SetListSong.objects.get(id=setlistsong_id)
                if request.POST[request_item] == u'Unassigned':
                    newset = 0
                else:
                    newset = int(request.POST[request_item])
                new_set = Set.objects.get(set_list_id=setlist_id, set_number=newset)
                setlistsong.set = new_set
                setlistsong.save()
    function = 'arrange'
    return render_to_response('setlist_detail.html',
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
