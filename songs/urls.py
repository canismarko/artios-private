from django.conf.urls import patterns, include, url

urlpatterns = patterns('songs.views',
                       url(r'^$', 'list'),
                       url(r'^order/(title|artist|band_singer|status)/', 'list'),
                       url(r'^add/$', 'edit'),
                       url(r'^(?P<song_id>\d+)/$', 'detail'),
                       url(r'^(?P<song_id>\d+)/modify/$', 'edit'),
                       url(r'^(?P<song_id>\d+)/(?P<function>lyrics|chords)/$', 'detail'),
                       url(r'^(?P<song_id>\d+)/(?P<function>lyrics|chords)/modify/$', 'edit'),
                       url(r'^setlists/$', 'setlists'),
                       url(r'^setlists/add/$', 'setlist_edit'),
                       url(r'^setlists/(?P<setlist_id>\d+)/$', 'setlist_detail'),
                       url(r'^setlists/(?P<setlist_id>\d+)/edit/$', 'setlist_edit'),
                       url(r'^setlists/(?P<setlist_id>\d+)/addremove/$', 'setlist_addremove'),
                       url(r'^setlists/(?P<setlist_id>\d+)/arrange/$', 'setlist_arrange'),
)
