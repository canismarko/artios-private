from django.db import models
from artios_privatesite.main.models import BandMember
import datetime

# Create your models here.
class Transaction(models.Model):
    date = models.DateField(default=datetime.date.today())
    member = models.ForeignKey(BandMember)
    description = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    active = models.BooleanField(default=True)
    def __unicode__(self):
        return u'%s ($%s)' % (self.date, self.amount)
