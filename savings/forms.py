from django import forms
from savings.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('date', 'member', 'amount', 'description')
