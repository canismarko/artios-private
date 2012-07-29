from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from artios_privatesite.tasks.models import Task
from artios_privatesite.tasks.forms import TaskForm


# Display a list of Artios tasks currently available
@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render_to_response('task_list.html', 
                              locals(), 
                              RequestContext(request))

# Displays a form to modify a task and then validates 
# and saves the updated object.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Artios').count() > 0)
def modify(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        # If valid then save and redirect back to task list
        if form.is_valid(): 
            form.save()
            return redirect('/tasks/')
    else: # New form
        form = TaskForm(instance=task)
    return render_to_response('modify.html', 
                              locals(),
                              RequestContext(request))

# Display a detailed view of a task
@login_required
def detail(request, task_id):
    return HttpResponse("Task detail " + task_id)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Artios').count() > 0)
# First ask to confirm and then actually delete a task from the Artios list
def delete(request, task_id):
    task = Task.objects.get(id=task_id)
    # Check if the user has confirmed they want to delete
    if 'confirm' in request.POST: 
        # test to see if the user clicked the "delete" button
        if '_delete' in request.POST:
            name = task.action
            next = 'Tasks'
            next_url = '/tasks/'
            try: # Perform the actual delete
                task.delete()
                return render_to_response('delete_confirmed.html', 
                                          locals(),
                                          RequestContext(request))
            except:
                return render_to_response('delete_failed.html', 
                                          locals(),
                                          RequestContext(request))
        else: # User did not click the 'delete' button (possibly cancel)
            return redirect('/tasks/')
    else: # We need to ask the user to confirm deletion
        name = task.action
        return render_to_response('delete_ask.html', 
                                  locals(),
                                  RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Artios').count() > 0)
# Let the user add a task (display a form or validate and store POST data)
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tasks/')
    else: # New form
        form = TaskForm()
    display = 'task'
    return render_to_response('add.html', 
                              locals(),
                              RequestContext(request))
