from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples
                       # url(r'^$', 'views.home', name='home'),
                       
                       # Uncomment the admin/doc line below to enable admin documentation
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login', login),
                       url(r'^accounts/logout', logout),

                       # Takes us to the tasks app
                       url('^$', 'main.views.home_redirect', name='home'),
                       url('^wp-admin/$', 'main.views.home_redirect', name='home'),
                       url('^tasks/', include('tasks.urls')),

                       # And the practice log app
                       url('^practice/', include('practicelog.urls')),

                       # and the album checksheet app
                       url('^worksheet/', include('worksheet.urls')),
                       
                       # App for the summary of the savings account
                       url('^savings/', include('savings.urls')),

                       # The meeting minutes app
                       url('^minutes/', include('minutes.urls')),

                       # Set lists app (songlist)
                       url('^songs/', include('songs.urls')),

                       # The calendar. This does not exist as an app 
                       # but rather lives in the 'main' module
                       url('^calendar/(artios|wss)/$', 'main.views.calendar'),

)

