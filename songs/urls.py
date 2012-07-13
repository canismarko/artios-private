from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('songs.views',
                       url(r'^$', 'list'),
                       url(r'^add/$', 'edit'),
                       url(r'^(\d+)/$', 'detail'),
                       url(r'^(\d+)/modify/$', 'edit'),
                       url(r'^(\d+)/(lyrics|chords)/$', 'detail'),
                       url(r'^(\d+)/(lyrics|chords)/modify/$', 'edit'),
)
