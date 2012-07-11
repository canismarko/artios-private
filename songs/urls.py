from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('songs.views',
                       url(r'^$', 'list'),
                       url(r'^add/$', 'add'),
                       url(r'^(\d+)/$', 'detail'),
                       url(r'^(\d+)/modify/$', 'edit'),
                       url(r'^(\d+)/lyrics/$', 'lyrics'),
                       url(r'^(\d+)/chords/$', 'chords'),
)
