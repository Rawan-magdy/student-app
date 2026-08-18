from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from dashboard.models import Activity
from django.http import HttpResponse
from .utils import render_to_pdf
from django.utils import timezone


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'planner/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)   
            task.user = request.user          
            task.save()                      
            Activity.objects.create(user=request.user, action=f"Created task: {task.title}")
            messages.success(request, "Task created successfully!")
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'planner/task_form.html', {'form': form, 'title': 'Add Task'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)   
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            Activity.objects.create(user=request.user, action=f"Updated task: {task.title}")
            messages.success(request, "Task updated!")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'planner/task_form.html', {'form': form, 'title': 'Edit Task'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        Activity.objects.create(user=request.user, action=f"Deleted task: {title}")
        messages.success(request, "Task deleted!")
        return redirect('task_list')
    return render(request, 'planner/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status == Task.Status.COMPLETED:
        task.status = Task.Status.PENDING
    else:
        task.status = Task.Status.COMPLETED
    task.save()
    return redirect('task_list')

@login_required
def tasks_pdf(request):
    tasks = Task.objects.filter(user=request.user)
    pdf = render_to_pdf('planner/tasks_pdf.html', {
        'tasks': tasks,
        'username': request.user.username,
        'date': timezone.now(),
    })
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="my_tasks.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=400)