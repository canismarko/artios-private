from django import forms
from artios_privatesite.tasks.models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget = forms.TextInput(attrs={'class': 'date'})
        )
    class Meta:
        model = Task
