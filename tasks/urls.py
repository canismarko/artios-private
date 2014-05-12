from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'tasks.views.task_list'),
                       url(r'^add/$', 'tasks.views.add_task'),
                       # Tasks are referenced by ID. These URLS parse for
                       #   a number and pass that on. URLs for details view,
                       #   modifying a task, and deleting a task.
                       url(r'^(\d+)/$', 'tasks.views.detail'),
                       url(r'^(\d+)/modify/$', 'tasks.views.modify'),
                       url(r'^(\d+)/delete/$', 'tasks.views.delete'),
)
