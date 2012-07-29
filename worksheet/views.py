from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import simplejson
from artios_privatesite.worksheet.models import Song, Milestone, MilestoneGroup, CompletionStatus, Completion
from artios_privatesite.worksheet.forms import *

# Displays a table of the album progress so far
@login_required
def overview(request):
    groups = request.user.groups.all()
    username = request.user.username
    count = request.user.groups.filter(name='Artios').count()
    # assert False
    song_list = Song.objects.order_by('recording_order')
    number_of_columns = Song.objects.count() + 1 # used by template
    # milestone_list = Milestone.objects.order_by('group')
    attribute_list = []
    # Set a row for each song attribute (recording order, bitrate, etc...)
    attribute_line = ['Recording order']
    for song in song_list:
        attribute_line.append(song.recording_order)
    attribute_list.append(attribute_line)
    attribute_line = ['Track number']
    for song in song_list:
        attribute_line.append(song.track_number)
    attribute_list.append(attribute_line)
    attribute_line = ['Tempo']
    for song in song_list:
        attribute_line.append(song.tempo)
    attribute_list.append(attribute_line)
    attribute_line = ['Bitrate']
    for song in song_list:
        attribute_line.append(song.bit_rate)
    attribute_list.append(attribute_line)
    attribute_line = ['Sample Rate']
    for song in song_list:
        attribute_line.append(song.sample_rate)
    attribute_list.append(attribute_line)
    # Now a list of milestone groups
    # Each entry will be a list of milestones (ea. editing, tracking, mixing)
    milestone_group_list = []
    milestone_groups = MilestoneGroup.objects.order_by('order')
    # Assemble the large list that contains all the remaining rows
    #   Will be a list that is several levels deep and gets parsed
    #   by the template.
    for group in milestone_groups:
        milestones = Milestone.objects.filter(group__id = group.id).order_by('order')
        milestones_list = []
        # For each row
        for milestone in milestones:
            milestone_status_list = [{'display': milestone.name,
                                      'milestone_id': milestone.id}]
            for song in song_list:
                try:
                    status = Completion.objects.get(milestone__id=milestone.id, song__id=song.id)
                    display = status.status.display
                    css_class = status.status.css_class
                    if css_class == None:
                        css_class = ""
                except:
                    display = u'&nbsp;'
                    css_class = ""
                milestone_status_list.append({'display': display,
                                              'milestone_id': milestone.id,
                                              'song_id': song.id,
                                              'css_class': css_class,
                                              })
            milestones_list.append(milestone_status_list)
        milestone_group_list.append({'group_name': group.name, 'group_row': milestones_list})
    # Now get the response
    return render_to_response('worksheet.html',
                              locals(), 
                              RequestContext(request))

# Ask the user which song and milestone he want to modify
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Artios').count() > 0)
def modify_prompt(request):
    # If the user has specified which song and milestone
    if request.method == 'POST':
        return_url = reverse(overview)
        song_name = Song.objects.get(id=int(request.POST['song']))
        milestone_name = Milestone.objects.get(id=int(request.POST['milestone']))
        if '_modify' in request.POST:
            # Perform the actual modifications
            try: # if object exists
                completion = Completion.objects.get(song=request.POST['song'],
                                                    milestone=request.POST['milestone'])
            except Completion.DoesNotExist:
                # if not, create a new one
                song = Song.objects.get(id=request.POST['song'])
                milestone = Milestone.objects.get(id=request.POST['milestone'])
                completion = Completion(song=song, milestone=milestone)
            form = StatusForm(request.POST, instance=completion)
            if form.is_valid():
                form.save()
                return redirect(return_url)
        if '_cancel' in request.POST:
            return redirect(return_url)
        else: # ask what the user wishes to change the status to
            buttons = [{'name': '_modify', 'value': 'Modify'},
                       {'name': '_cancel', 'value': 'Cancel'}]
            try:
                completion = Completion.objects.get(song=request.POST['song'],
                                                    milestone=request.POST['milestone'])
                form = StatusForm(instance=completion, initial={'song': request.POST['song'], 
                                                                'milestone': request.POST['milestone']})
            except:
                form = StatusForm(initial={'song': request.POST['song'],
                                           'milestone': request.POST['milestone']})
            return render_to_response('modify.html',
                                      locals(),
                                      RequestContext(request))
    else: # Ask which entry to modify
        form = StatusPromptForm()
        display = 'status'
    return render_to_response('modify.html',
                              locals(),
                              RequestContext(request))

# Allows the user the change the status of a Completion object
#   returns the new display string (primarily used for AJAX calls).
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Artios').count() > 0)
def ajax_status(request, song_id, milestone_id):
    # Get the current status or create a new one if it doesn't exist
    try:
        completion = Completion.objects.get(song__id=song_id, milestone__id=milestone_id)
    except Completion.DoesNotExist:
        song = Song.objects.get(id=song_id)
        milestone = Milestone.objects.get(id=milestone_id)
        status = CompletionStatus.objects.get(id=1)
        completion = Completion(song=song, milestone=milestone, status=status)
    # Set some variables and determine the new status
    current_status_id = completion.status.id
    total_status_count = CompletionStatus.objects.count()
    if current_status_id == total_status_count:
        new_status_id = 1
    else:
        new_status_id = current_status_id + 1
    new_status = CompletionStatus.objects.get(id=new_status_id)
    completion.status = new_status
    # Send the response
    css_class = 'colmain'
    if completion.status.css_class:
        css_class += ' ' + completion.status.css_class
    response_dict = {'html': completion.status.display, 'css_class': css_class}
    json_response = simplejson.dumps(response_dict)
    try:
        completion.full_clean()
        completion.save()
        return HttpResponse(json_response)
    except:
        assert False
