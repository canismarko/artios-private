from django.conf.urls import patterns, include, url

urlpatterns = patterns('worksheet.views',
                       url(r'^$', 'overview'),
                       url(r'^modify/$', 'modify_prompt'),
                       url(r'^ajax/incrementstatus/(?P<song_id>\d+)/(?P<milestone_id>\d+)/$', 'ajax_status'),
)
