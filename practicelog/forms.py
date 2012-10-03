from django import forms
from practicelog.models import PracticeEntry

class PracticeForm(forms.ModelForm):
    timestamp = forms.DateField(
        widget = forms.TextInput(attrs={'class':'date'})
        )
    class Meta:
        model = PracticeEntry
