from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from artios_privatesite.savings.models import Transaction
from artios_privatesite.savings.forms import TransactionForm

# Display the summary of the account
@login_required
def overview(request):
    transactions = Transaction.objects.order_by('date')
    transaction_list = []
    balance = 0
    # We need to tweak a few display settings so the transaction_list is transferred to a new dictionary
    for transaction in transactions:
        transaction_entry = {}
        transaction_entry['id'] = transaction.id
        transaction_entry['active'] = transaction.active
        transaction_entry['date'] = transaction.date
        transaction_entry['description'] = transaction.description
        # Test for positive or negative display
        if transaction.amount < 0:
            transaction_entry['amount'] = "-$%.2f" % -transaction.amount
        else:
            transaction_entry['amount'] = "$%.2f" % transaction.amount
        if transaction.active == True:
            balance += transaction.amount
        transaction_list.append(transaction_entry)
    # Test for a positive or negative balance
    if balance < 0:
        balance_display = "-$%.2f" % -balance
    else:
        balance_display = "$%.2f" % balance
    return render_to_response('account_overview.html',
                              locals(),
                              RequestContext(request))

# Add a new transaction as detailed by the user
@login_required
def add(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/savings/')
    else: # New form
        form = TransactionForm()
    display = 'transaction'
    return render_to_response('add.html',
                              locals(),
                              RequestContext(request))

# Toggle whether a transaction is active
@login_required
def toggle(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    if transaction.active == True:
        transaction.active = False
    else:
        transaction.active = True
    transaction.save()
    return redirect('/savings/')
