import copy

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, HistoricalTaskEvent
from .froms import TaskForm


forbidden_list = ['_state', '_django_version', 'id', 'assigned_user_id']


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


def task_create_new(request):
    if request.method == 'POST':
        task_creation_form = TaskForm(request.POST)

        if task_creation_form.is_valid():
            task = task_creation_form.save(commit=False)
            current_user = request.user.username if request.user.username != '' else 'Anonymous'
            task.author = current_user
            task.save()

            event = HistoricalTaskEvent.objects.create(user_who_edited=current_user)
            event.task = task

            fields = set([atr for atr, value in task.__dict__.items() if atr not in forbidden_list])
            field_to_update, old_value, new_value = [], [], []
            for atr in fields:
                field_to_update.append(atr)
                old_value.append('---')
                new_value.append(task.__dict__[atr])
            event.field_to_update = field_to_update
            event.old_value = old_value
            event.new_value = new_value
            event.save()

            return redirect('task_list')
    else:
        task_creation_form = TaskForm()

    return render(request, 'task_edit.html', {'form': task_creation_form})


def task_details(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_details.html', {'task': task})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_old = copy.copy(task)
    if request.method == "POST":
        task_edit_form = TaskForm(request.POST, instance=task)

        if task_edit_form.is_valid():
            current_user = request.user.username if request.user.username != '' else 'Anonymous'

            task = task_edit_form.save(commit=False)
            task.save()

            event = HistoricalTaskEvent.objects.create(user_who_edited=current_user)

            fields_where_change_occurred = set([atr for atr, value in
                                                task_old.__dict__.items() ^ task.__dict__.items()
                                                if atr not in forbidden_list])

            field_to_update, old_value, new_value = [], [], []
            for atr in fields_where_change_occurred:
                field_to_update.append(atr)
                old_value.append(task_old.__dict__[atr])
                new_value.append(task.__dict__[atr])
            event.field_to_update = field_to_update
            event.old_value = old_value
            event.new_value = new_value

            event.task = task
            event.save()

            return redirect('task_details', pk=task.pk)
    else:
        task_edit_form = TaskForm(instance=task)

    return render(request, 'task_edit.html', {'form': task_edit_form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')


def task_history(request):
    task_events = HistoricalTaskEvent.objects.all().order_by('-occurrence_date')
    return render(request, 'task_history.html', {'events': task_events})
