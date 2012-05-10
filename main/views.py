from django.shortcuts import redirect, render
# Create your views here.

def home_redirect(request):
    return redirect('/tasks/')

def calendar(request):
    return render(request, 'calendar.html')
