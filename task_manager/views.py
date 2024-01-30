from django.shortcuts import render, redirect
from .models import Task
from .froms import TaskForm


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


def create_new_task(request):
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
