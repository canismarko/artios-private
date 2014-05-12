from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'savings.views.overview'),
                       url(r'^add/$', 'savings.views.add'),
                       url(r'^toggle/(\d+)/$', 'savings.views.toggle'),
)
