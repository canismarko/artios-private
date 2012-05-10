from django.db import models

class Minutes(models.Model):
    date = models.DateField()
    toc = models.TextField()
    content = models.TextField()
    def __unicode__(self):
        return unicode(self.date)
    class Meta:
        ordering = ['-date']
