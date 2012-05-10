from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples
                       # url(r'^$', 'artios_privatesite.views.home', name='home'),
                       # url(r'^artios_privatesite/', include('artios_privatesite.foo.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login', login),
                       url(r'^accounts/logout', logout),

                       # Takes us to the tasks app
                       url('^$', 'artios_privatesite.main.views.home_redirect', name='home'),
                       url('^tasks/', include('artios_privatesite.tasks.urls')),

                       # And the practice log app
                       url('^practice/', include('artios_privatesite.practicelog.urls')),

                       # and the album checksheet app
                       url('^worksheet/', include('artios_privatesite.worksheet.urls')),
                       
                       # App for the summary of the savings account
                       url('^savings/', include('artios_privatesite.savings.urls')),

                       # The meeting minutes app
                       url('^minutes/', include('artios_privatesite.minutes.urls')),
)
