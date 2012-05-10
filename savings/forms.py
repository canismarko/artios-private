from django import forms
from artios_privatesite.savings.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('date', 'member', 'amount', 'description')
