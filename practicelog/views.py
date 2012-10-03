# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
import time
from main.models import BandMember
from practicelog.forms import PracticeForm
from practicelog.models import PracticeEntry

# If no year and week is given, then redirect assuming today's values
# This ensures that any links that assume a year and month will still work
@login_required
def practice_log_redirect(request):
    year = date.today().year
    week = date.today().strftime("%W")
    return redirect(str(year) + '/' + week + '/')

# Shows a table summarizing the practice log for a selected week
@login_required
def weeklysummary(request, 
                  year = date.today().year,
                  week = date.today().strftime("%W")):
    # Set some variables that describe the date-environment we're looking at
    week = int(week)
    year = int(year)
    monday = time.mktime(time.strptime( \
            str(year) + ' ' + str(week) + ' 1',\
            '%Y %W %w')) # Monday serves as common reference
    today_url = str(date.today().year) + '/' + str(date.today().strftime("%W"))
    # Set variables that control forward and back week buttons
    if week == 0:
        last_week = str(year-1) + '/52'
    else:
        last_week = str(year) + '/' + str(week-1)
    if week == 52:
        next_week = str(year+1) + '/0'
    else:
        next_week = str(year) + '/' + str(week+1)
    days_of_the_week = [] # 7 member list that holds the days of the week
    for x in range(0,7):
        day = monday + (86400*(x))
        days_of_the_week.append(time.strftime('%d %b', time.localtime(day)))
    practice_log = [] # This will be a list of lists discribing each day's time
    band_members = BandMember.objects.all()
    # Calculate the table for each band member
    for member in band_members:
        members_entries = []
        member_url = reverse(practice_log_redirect) + 'member/' + str(member.id) + '/'
        members_entries.append({'modify_url': member_url, 'total': member.display_name})
        weekly_total = 0
        for x in range(0,7): # For each day
            # Get all the practice entries for this member and day
            day = time.gmtime(monday + (86400*x))
            test_year = int(time.strftime('%Y', day))
            test_month = int(time.strftime('%m', day))
            test_day = int(time.strftime('%d', day))
            test_date = date(test_year, test_month, test_day)
            modify_url = '../../' + str(test_year) + '/' + str(test_month) + '/' + str(test_day) + '/'
            entries = PracticeEntry.objects.filter(member=member)
            entries = entries.filter(timestamp=test_date)
            total = 0
            for entry in entries:
                if entry.duration > 0:
                    total += entry.duration
            members_entries.append({'modify_url': modify_url, 'total': total})
            weekly_total += total
        # Tag on an entry for the cumulative total for the week and total points (over all time)
        members_entries.append({'modify_url': 'TODO', 'total': weekly_total})
        points_entries = PracticeEntry.objects.filter(member=member)
        points_entries = points_entries.filter(points=True)
        points_total = 0
        for points_entry in points_entries:
            points_total += points_entry.duration
        members_entries.append({'modify_url': 'TODO', 'total': points_total})
        # Add this members time to total log
        practice_log.append(members_entries) 
    return render_to_response('practicelog.html', 
                              locals())

def spend(request, member='none'):
    return HttpResponse("Here goes the spend dialog for " + member)

# The user will add some practice time
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Artios').count() > 0)
def add(request):
    # If form was submitted...
    if request.method == 'POST':
        form = PracticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/practice/')
    else: # ...else new form
        form = PracticeForm()
    display = 'practice entry'
    return render_to_response('add.html',
                              locals(),
                              RequestContext(request))

# Display a list that allows the user to modify the entries
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Artios').count() > 0)
def modify(request, year, month, day):
    today = date(int(year), int(month), int(day))
    date_string = today.strftime("%d %b %Y")
    # If user has submitted a form
    if request.method == 'POST':
        week = today.strftime("%W")
        # return_url holds a string to redirect to when 'cancel' buttons are clicked or valid submission
        return_url = reverse(practice_log_redirect) + str(year) + '/' + week + '/'
        # Check if we're modifying...
        if '_modify' in request.POST:
            entry = PracticeEntry(id=request.POST['modify_id'])
            form = PracticeForm(request.POST, instance=entry)
            if form.is_valid():
                form.save()
                return redirect(return_url)
            else:
                form_list = [{'form': form, 'id': request.POST['modify_id']}]
        # ...or if we're deleting...
        elif '_delete' in request.POST:
            entry = PracticeEntry.objects.get(id=request.POST['modify_id'])
            # If user has already confirmed, then delete
            if 'confirm' in request.POST:
                if '_delete' in request.POST:
                    entry.delete()
                return redirect(return_url)
            else: # Has not confirmed. Ask to confirm.
                name_list = [str(entry.timestamp)]
                name_duration = str(entry.duration) + ' hour'
                if entry.duration != 1:
                    name_duration += 's'
                name_list.append(name_duration)
                name_list.append(entry.description)
                entry_id = request.POST['modify_id']
                return render_to_response('delete_ask.html',
                                          locals(),
                                          RequestContext(request))
        # ...or 'cancel' was clicked.
        else:
            return redirect(return_url)
    else: # Display the full list for the day
        entries_list = PracticeEntry.objects.filter(timestamp = date(int(year), int(month), int(day)))
        form_list = []
        for entry in entries_list:
            form = PracticeForm(instance=entry)
            form_list.append({'form': form, 'id': entry.id})
    return render_to_response('modify_list.html',
                              locals(),
                              RequestContext(request))

# Sort out the practice log entries for a specific member
@login_required
def list_by_member(request, member_id):
    member = BandMember.objects.get(id=member_id)
    entry_list = PracticeEntry.objects.filter(member__id=member_id)
    entry_list = entry_list.order_by('timestamp')
    return render_to_response('practicelog_list.html',
                              locals())
