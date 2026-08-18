from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Note, Category
from .forms import NoteForm, CategoryForm
from dashboard.models import Activity


@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)

    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category_id:
        notes = notes.filter(category_id=category_id)

    paginator = Paginator(notes, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    categories = Category.objects.filter(user=request.user)
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'notes/note_list.html', context)


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            form.save_m2m()   
            Activity.objects.create(user=request.user, action=f"Created note: {note.title}")
            messages.success(request, "Note created!")
            return redirect('note_list')
    else:
        form = NoteForm(user=request.user)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Add Note'})


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()   
            messages.success(request, "Note updated!")
            return redirect('note_list')
    else:
        form = NoteForm(instance=note, user=request.user)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Edit Note'})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        title = note.title
        note.delete()
        Activity.objects.create(user=request.user, action=f"Deleted note: {title}")
        messages.success(request, "Note deleted!")
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            messages.success(request, "Category added!")
            return redirect('note_list')
    else:
        form = CategoryForm()
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Add Category'})