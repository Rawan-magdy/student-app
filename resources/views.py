from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Resource, ResourceType
from .forms import ResourceForm
from dashboard.models import Activity


@login_required
def resource_list(request):
    resources = Resource.objects.filter(user=request.user)

    query = request.GET.get('q', '')
    type_id = request.GET.get('type', '')

    if query:
        resources = resources.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if type_id:
        resources = resources.filter(resource_type_id=type_id)

    paginator = Paginator(resources, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    types = ResourceType.objects.all()
    return render(request, 'resources/resource_list.html', {
        'page_obj': page_obj,
        'types': types,
        'query': query,
        'selected_type': type_id,
    })


@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.user = request.user
            resource.save()
            Activity.objects.create(user=request.user, action=f"Added resource: {resource.title}")
            messages.success(request, "Resource added!")
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'resources/resource_form.html', {'form': form, 'title': 'Add Resource'})


@login_required
def resource_update(request, pk):
    resource = get_object_or_404(Resource, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource updated!")
            return redirect('resource_list')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resources/resource_form.html', {'form': form, 'title': 'Edit Resource'})


@login_required
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk, user=request.user)
    if request.method == 'POST':
        title = resource.title
        resource.delete()
        Activity.objects.create(user=request.user, action=f"Deleted resource: {title}")
        messages.success(request, "Resource deleted!")
        return redirect('resource_list')
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})