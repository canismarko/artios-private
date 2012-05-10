from django.contrib import admin
from artios_privatesite.worksheet.models import *

admin.site.register(Song)
admin.site.register(Milestone)
admin.site.register(MilestoneGroup)
admin.site.register(CompletionStatus)
admin.site.register(Completion)

