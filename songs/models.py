from django.db import models
from django.contrib.auth.models import Group
from artios_privatesite.main.models import BandMember

class SongStatus(models.Model):
    display = models.CharField(max_length=50)
    def __unicode__(self):
        return self.display

# Describes a song that will be in a set list
class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100, blank=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    band_singer = models.ForeignKey(BandMember, blank=True, null=True)
    tempo = models.CharField(max_length=20, blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    chords = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    band = models.ForeignKey(Group)
    status = models.ForeignKey(SongStatus)
    class Meta:
        ordering = ('order',)
    def __unicode__(self):
        return self.title
