from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from planner.models import Task
from notes.models import Note, Category
from resources.models import Resource
from .models import Activity


@login_required
def dashboard_view(request):
    user = request.user

    tasks = Task.objects.filter(user=user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status=Task.Status.COMPLETED).count()
    pending_tasks = tasks.filter(status=Task.Status.PENDING).count()

    total_notes = Note.objects.filter(user=user).count()
    total_resources = Resource.objects.filter(user=user).count()

    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    upcoming_tasks = tasks.filter(
        status=Task.Status.PENDING,
        due_date__range=[today, next_week]
    ).order_by('due_date')

    recent_activities = Activity.objects.filter(user=user)[:5]

    progress = 0
    if total_tasks > 0:
        progress = round((completed_tasks / total_tasks) * 100)

    status_data = [completed_tasks, pending_tasks]
    priority_data = [
        tasks.filter(priority=Task.Priority.LOW).count(),
        tasks.filter(priority=Task.Priority.MEDIUM).count(),
        tasks.filter(priority=Task.Priority.HIGH).count(),
    ]
    categories = Category.objects.filter(user=user)
    category_labels = [c.name for c in categories]
    category_data = [c.notes.count() for c in categories]

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'total_notes': total_notes,
        'total_resources': total_resources,
        'upcoming_tasks': upcoming_tasks,
        'recent_activities': recent_activities,
        'progress': progress,
        'status_data': status_data,
        'priority_data': priority_data,
        'category_labels': category_labels,
        'category_data': category_data,
        'category_labels_raw': category_labels,
    }
    return render(request, 'dashboard/dashboard.html', context)