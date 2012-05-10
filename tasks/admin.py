from django.contrib import admin
from artios_privatesite.tasks.models import Status, Task

admin.site.register(Status)
admin.site.register(Task)
