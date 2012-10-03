from datetime import date
from django.db import models
from django.contrib.auth.models import Group
from main.models import BandMember

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
    status = models.ForeignKey(SongStatus, blank=True, null=True)
    class Meta:
        ordering = ('order',)
    def __unicode__(self):
        return self.title

class SetList(models.Model):
    '''
    Model describes a set list for (generally) one show.
    It holds a few pieces of data regarding the set-list
    itself. Multiple Set objects then refer back to a set list.
    '''
    name = models.CharField(max_length=200)
    date = models.DateField(default=date.today())
    location = models.CharField(max_length=200, blank=True, null=True)
    band = models.ForeignKey(Group)
    pay = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=6)
    notes = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ('date',)
    def __unicode__(self):
        return str(self.date) + ' - ' + self.name

class Set(models.Model):
    '''
    Holds a group of songs. Each Set object refers
    back to to a SetList object via a primary key relationship.
    '''
    set_list = models.ForeignKey(SetList)
    set_number = models.IntegerField()
    songs = models.ManyToManyField(Song, through='SetListSong')
    class Meta:
        ordering = ('set_list', 'set_number')
    def __unicode__(self):
        return self.set_list.name + ' - Set ' + str(self.set_number)
    

class SetListSong(models.Model):
    '''
    This class describes a song on a set list.
    Used with the 'through' argument to a ManyToManyField
    ManyToMany fields relating a song and one for a
    SetList. There is also a numeric field containing
    the order.
    '''
    song = models.ForeignKey(Song)
    set = models.ForeignKey(Set)
    order = models.IntegerField()
    class Meta:
        ordering = ('set', 'order')
    def __unicode__(self):
        return str(self.set.set_list.name) + ' [' + str(self.order) + '] ' + self.song.title
