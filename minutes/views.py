from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from artios_privatesite.minutes.models import Minutes
from HTMLParser import HTMLParser

# This class redefines the html parser to change links in the TOC
class MinutesHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'href':
                attr[1] = u'1/' + attr[1]
                assert False

@login_required
def minutes_list(request):
    minutes_list = Minutes.objects.all()
    # We need to parse the toc in order to make the links correct
    for minutes in minutes_list:
        minutes.toc = minutes.toc.replace(u'#sec', unicode(minutes.id)+u'/#sec')
    return render_to_response('minutes_overview.html',
                              locals(),
                              RequestContext(request))

def minutes_detail(request, minutes_id):
    minutes = Minutes.objects.get(id = minutes_id)
    return render_to_response('minutes_detail.html',
                              locals(),
                              RequestContext(request))
                              
