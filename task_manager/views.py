from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .froms import TaskForm


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


def task_create_new(request):
    if request.method == 'POST':
        task_creation_form = TaskForm(request.POST)

        if task_creation_form.is_valid():
            task = task_creation_form.save(commit=False)
            task.author = request.user.username if request.user.username is not '' else 'Anonymous'
            # task.task_history.
            task.save()
            return redirect('/')
    else:
        task_creation_form = TaskForm()

    return render(request, 'task_edit.html', {'form': task_creation_form})


def task_details(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_details.html', {'task': task})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task_edit_form = TaskForm(request.POST, instance=task)

        if task_edit_form.is_valid():
            post = task_edit_form.save(commit=False)
            post.author = request.user.username
            post.save()
            return redirect('task_details', pk=post.pk)
    else:
        task_edit_form = TaskForm(instance=task)

    return render(request, 'task_edit.html', {'form': task_edit_form})
