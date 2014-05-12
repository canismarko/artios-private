from django.conf.urls import patterns, include, url

urlpatterns = patterns('practicelog.views',
                       url(r'^$', 'practice_log_redirect'),
                       url(r'^(?P<year>\d{4})/(?P<week>\d{1,2})/$', 'weeklysummary'), # go to a particular year and week
                       # Allows for spending practice points
                       #   Prompt for band member if none specified
                       url(r'^spend/$', 'spend'),
                       url(r'^spend/(?P<member>[^/]+)/$', 'spend'),
                       # Adds a practicing entry
                       url(r'^add/$', 'add'),
                       # Allows for modifying the practice log
                       url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'modify'),
                       url(r'^member/(\d)/', 'list_by_member'),
)
