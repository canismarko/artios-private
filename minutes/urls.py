from django.conf.urls import patterns, include, url

urlpatterns = patterns('minutes.views',
                       url(r'^$', 'minutes_list'),
                       url(r'^(\d+)/$', 'minutes_detail'),
)
