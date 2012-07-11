from django.db import models
# from artios_privatesite import songs

# Create your models here.

# This app shows a checksheet regarding album completion
# It links a song and a milestone which then combine
#  in a "completed" relation.

# Describes a song that will be tracked
class Song(models.Model):
    title = models.CharField(max_length=100)
    recording_order = models.IntegerField(blank=True, null=True)
    track_number = models.IntegerField(blank=True, null=True)
    tempo = models.CharField(max_length=20, blank=True, null=True)
    bit_rate = models.CharField(max_length=20, blank=True, null=True)
    sample_rate = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        ordering = ('recording_order',)
    def __unicode__(self):
        return self.title

# Allows for the grouping of milestones
#  eg. "tracking", "editing", "mixing"
class MilestoneGroup(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()
    class Meta:
        ordering = ('order',)
    def __unicode__(self):
        return self.name

# Decidable completion steps
#  eg. "drums", "editing guitar", etc
class Milestone(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(MilestoneGroup)
    order = models.IntegerField()
    class Meta:
        ordering = ('group__order', 'order')
    def __unicode__(self):
        return self.name + ' - ' + self.group.name

# Describes the possible states a song/milestone combination
#   can have.
class CompletionStatus(models.Model):
    name = models.CharField(max_length=50)
    # How should this status be displayed in the worksheet
    display = models.CharField(max_length=10)
    css_class = models.CharField(max_length=50, blank=True, null=True)
    def __unicode__(self):
        return self.name

# Holds the status of each song/milestone combination
# Non-existent combinations are assumed to be incomplete
class Completion(models.Model):
    song = models.ForeignKey(Song)
    milestone = models.ForeignKey(Milestone)
    status = models.ForeignKey(CompletionStatus)
    def __unicode__(self):
        return self.song.title + ' - ' + self.milestone.name
