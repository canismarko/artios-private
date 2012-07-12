from django import forms
from artios_privatesite.worksheet.models import Completion

class StatusPromptForm(forms.ModelForm):
    class Meta:
        model = Completion
        exclude = ('status',)

# For modifying a song's status
class StatusForm(forms.ModelForm):
    song = forms.IntegerField(widget=forms.HiddenInput)
    milestone = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Completion
        exclude = ('song', 'milestone')
