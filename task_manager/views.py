import copy

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task, HistoricalTaskEvent
from .froms import TaskForm, FilterTaskForm, FilterHistoryForm

forbidden_list = ['_state', '_django_version', 'id']
map_value = 'assigned_user_id'


def task_list(request):
    tasks = Task.objects.all()[::-1]
    if request.method == 'POST':
        filter_task_form = FilterTaskForm(request.POST)
        if filter_task_form.is_valid():
            result = filter_task_form.save(commit=False).phrase_string

            chosen_field_for_filtering = request.POST.get('field_to_be_filtered')
            if chosen_field_for_filtering == 'name_description':
                tasks = (Task.objects.filter(name__icontains=result) | Task.objects.filter(description__icontains=result))[::-1]
            elif chosen_field_for_filtering == 'status':
                tasks = Task.objects.filter(status__icontains=result)[::-1]
            elif chosen_field_for_filtering == 'assigned_user':
                tasks = Task.objects.filter(assigned_user__username__icontains=result)[::-1]

    else:
        filter_task_form = FilterTaskForm()

    return render(request, 'task_list.html', {'tasks': tasks, 'form': filter_task_form})


def task_create_new(request):
    if request.method == 'POST':
        task_creation_form = TaskForm(request.POST)

        if task_creation_form.is_valid():
            task = task_creation_form.save(commit=False)
            current_user = request.user.username if request.user.username != '' else 'Anonymous'
            task.author = current_user
            task.save()

            event = HistoricalTaskEvent.objects.create(task_id=task.id, task_name=task.name,
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

            event = HistoricalTaskEvent.objects.create(task_id=task.id, task_name=task.name,
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
    event = HistoricalTaskEvent.objects.create(task_id=task.id, task_name=task.name,
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

    task.delete()
    event.save()

    return redirect('task_list')


def task_history(request):
    task_events = HistoricalTaskEvent.objects.all().order_by('-occurrence_date')
    display_detailed_history_url_button = False
    the_one_task = None
    timezone_from_datetimefield = None

    if request.method == 'POST':
        filter_history_form = FilterHistoryForm(request.POST)
        if filter_history_form.is_valid():
            task = filter_history_form.save(commit=False).task
            if task != None:
                dt = request.POST.get('task_state_till_date')
                timezone_from_datetimefield = timezone.make_aware(
                    timezone.datetime.strptime(dt, '%Y-%m-%dT%H:%M'),
                    timezone.get_default_timezone()
                )

                task_events = (HistoricalTaskEvent.objects.filter(task_id=task.id)
                               .filter(occurrence_date__lte=timezone_from_datetimefield)
                               .order_by('-occurrence_date'))

                display_detailed_history_url_button = True
                the_one_task = task

    else:
        filter_history_form = FilterHistoryForm()

    return render(request, 'task_history.html', {'events': task_events,
                                                 'form': filter_history_form,
                                                 'display_detailed_url': display_detailed_history_url_button,
                                                 'task': the_one_task,
                                                 'state_date': timezone_from_datetimefield})


def task_history_details(request, pk, time):
    task = get_object_or_404(Task, pk=pk)
    archival_task = Task()

    events_related_to_task_before_the_set_time = (HistoricalTaskEvent.objects
                                                  .filter(task_id=task.id)
                                                  .filter(occurrence_date__lte=time)
                                                  .order_by('occurrence_date'))
    for event in events_related_to_task_before_the_set_time:
        if event.fields_to_update != None or event.new_values != None:
            for field, new_value in zip(event.fields_to_update, event.new_values):
                archival_task.__dict__[field] = new_value

    return render(request, 'task_history_details.html',
                  {'archival_task': archival_task, 'time': time})
