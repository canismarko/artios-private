from django import forms
from artios_privatesite.practicelog.models import PracticeEntry

class PracticeForm(forms.ModelForm):
    timestamp = forms.DateField(
        widget = forms.TextInput(attrs={'class':'date'})
        )
    class Meta:
        model = PracticeEntry
