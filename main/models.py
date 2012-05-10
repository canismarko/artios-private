from django.db import models

# Create your models here.

class BandMember(models.Model):
    # Describes a band member. Supplies foreign keys to various 
    # other models.
    full_name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.display_name
