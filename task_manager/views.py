import copy

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from task_manager.models import Task, HistoricalTaskEvent
from .froms import TaskForm
from .filters import TaskFilter, HistoricalTaskEventFilter

forbidden_list = ['_state', '_django_version', 'id']
map_value = 'assigned_user_id'


def task_list(request):
    task_filter = TaskFilter(request.POST, queryset=Task.objects.all())
    return render(request, 'task_list.html', {'tasks': task_filter.qs[::-1], 'form': task_filter.form})


def task_create_new(request):
    if request.method == 'POST':
        task_creation_form = TaskForm(request.POST)

        if task_creation_form.is_valid():
            task = task_creation_form.save(commit=False)
            current_user = request.user.username if request.user.username != '' else 'Anonymous'
            task.author = current_user
            task.save()

            event = HistoricalTaskEvent.objects.create(task=task, historical_task_id=task.id, task_name=task.name,
                                                       user_who_edited=current_user)
            event.action = 'Create'
            assigned_user = task.assigned_user.username if task.assigned_user != None else '---'
            event.assigned_user = assigned_user

            fields = set([atr for atr, value in task.__dict__.items() if atr not in forbidden_list])
            fields_to_update, old_values, new_values = [], [], []
            if map_value in fields:
                fields.remove(map_value)
                fields_to_update.append('assigned user')
                old_values.append('---')
                new_values.append(assigned_user)

            for atr in fields:
                fields_to_update.append(atr)
                old_values.append('---')
                new_values.append(task.__dict__[atr])
            event.fields_to_update = fields_to_update
            event.old_values = old_values
            event.new_values = new_values

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

            event = HistoricalTaskEvent.objects.create(task=task, historical_task_id=task.id, task_name=task.name,
                                                       user_who_edited=current_user)
            event.action = 'Update'
            assigned_user = task.assigned_user.username if task.assigned_user != None else '---'
            event.assigned_user = assigned_user

            fields_where_change_occurred = set([atr for atr, value in
                                                task_old.__dict__.items() ^ task.__dict__.items()
                                                if atr not in forbidden_list])
            fields_to_update, old_values, new_values = [], [], []
            if map_value in fields_where_change_occurred:
                fields_where_change_occurred.remove(map_value)
                fields_to_update.append('assigned user')
                old_values.append(task_old.assigned_user.username if task_old.assigned_user != None else '---')
                new_values.append(assigned_user)

            for atr in fields_where_change_occurred:
                fields_to_update.append(atr)
                old_values.append(task_old.__dict__[atr])
                new_values.append(task.__dict__[atr])
            event.fields_to_update = fields_to_update
            event.old_values = old_values
            event.new_values = new_values

            event.save()

            return redirect('task_details', pk=task.pk)
    else:
        task_edit_form = TaskForm(instance=task)

    return render(request, 'task_edit.html', {'form': task_edit_form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    current_user = request.user.username if request.user.username != '' else 'Anonymous'
    event = HistoricalTaskEvent.objects.create(task=task, historical_task_id=task.id, task_name=task.name,
                                               user_who_edited=current_user)
    event.action = 'Delete'
    assigned_user = task.assigned_user.username if task.assigned_user != None else '---'
    event.assigned_user = assigned_user

    fields = set([atr for atr, value in task.__dict__.items() if atr not in forbidden_list])
    fields_to_update, old_values, new_values = [], [], []
    if map_value in fields:
        fields.remove(map_value)
        fields_to_update.append('assigned user')
        old_values.append(assigned_user)
        new_values.append('---')

    for atr in fields:
        fields_to_update.append(atr)
        old_values.append(task.__dict__[atr])
        new_values.append('---')
    event.fields_to_update = fields_to_update
    event.old_values = old_values
    event.new_values = new_values

    event.save()
    task.delete()

    return redirect('task_list')


def task_history(request):
    task_events_filter = HistoricalTaskEventFilter(request.POST,
                                            queryset=HistoricalTaskEvent.objects.all().order_by('-occurrence_date'))
    display_detailed_history_url_button = False
    the_one_task = None
    timezone_from_datetimefield = None

    if request.method == 'POST':
        pk = task_events_filter.data.get('task')
        if pk.isdigit():
            task = get_object_or_404(Task, pk=pk)
            if task != None:
                display_detailed_history_url_button = True
                the_one_task = task
                time_f = task_events_filter.data.get('occurrence_date')
                timezone_from_datetimefield = time_f if time_f != '' else timezone.now()

    return render(request, 'task_history.html', {'events': task_events_filter.qs,
                                                 'form': task_events_filter.form,
                                                 'display_detailed_url': display_detailed_history_url_button,
                                                 'task': the_one_task,
                                                 'state_date': timezone_from_datetimefield})


def task_history_details(request, pk, time):
    task = get_object_or_404(Task, pk=pk)
    archival_task = Task()

    events_related_to_task_before_the_set_time = (HistoricalTaskEvent.objects
                                                  .filter(historical_task_id=task.id)
                                                  .filter(occurrence_date__lte=time)
                                                  .order_by('occurrence_date'))
    for event in events_related_to_task_before_the_set_time:
        if event.fields_to_update != None or event.new_values != None:
            for field, new_value in zip(event.fields_to_update, event.new_values):
                archival_task.__dict__[field] = new_value

    return render(request, 'task_history_details.html',
                  {'archival_task': archival_task, 'time': time})
