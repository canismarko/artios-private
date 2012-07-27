from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

def home_redirect(request):
    return redirect('/songs/')

# Displays pages with iframe for various calendars
def calendar(request, calendar):
    if calendar == "wss":
        source = "https://www.google.com/calendar/embed?src=westernsoundstudios%40gmail.com&ctz=America/New_York"
    elif calendar == "artios":
        source = "https://www.google.com/calendar/embed?src=artiosband%40gmail.com&ctz=America/New_York"
    return render_to_response('calendar.html',
                              locals(),
                              RequestContext(request))
