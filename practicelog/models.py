from django.db import models
from main.models import BandMember

# Create your models here.
class PracticeEntry(models.Model):
    # Hold one instance of a user practicing
    timestamp = models.DateField() # when he practiced
    member = models.ForeignKey(BandMember) # who practiced
    description = models.TextField() # what was practiced
    duration = models.FloatField() # how long it was practiced
    points = models.BooleanField() # wether it is eligible for practice points
    def __unicode__(self):
        return self.description
    
