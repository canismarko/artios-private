from django.db import models
from main.models import BandMember

# Describes the possible status a task can have
class Status(models.Model):
      description = models.CharField(max_length=300)
      # Used in the 'class=""' attribute in the HTML
      #  the actual appearance is done with stylesheets later on
      css_class = models.CharField(max_length=50)
      def __unicode__(self):
            return self.description

class Task(models.Model):
      # Holds an Artios task assigned to a band member
      assignee = models.ForeignKey(BandMember)
      status = models.ForeignKey(Status)
      due_date = models.DateField()
      action = models.CharField(max_length=300)
      comments = models.TextField(blank=True)
      def __unicode__(self):
            return self.action
