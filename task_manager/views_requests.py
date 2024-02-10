import copy
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task, HistoricalTaskEvent
from .froms import TaskForm, FilterTaskForm, FilterHistoryForm
from .filters import TaskFilter, HistoricalTaskEventFilter
from os import environ as envs
from os.path import join

forbidden_list = ['_state', '_django_version', 'id']
map_value = 'assigned_user_id'
ROOT_ENDPOINT = 'http://localhost:{}/api/' \
                    .format(envs['MY_WEB_APP_EXTERNAL_PORT'] if 'is_docker_running_env_variable' in envs else '8000')


def task_list(request):
    tasks = None
    filter_task_form = None

    if request.method == 'GET':
        tasks = requests.get(ROOT_ENDPOINT + 'task/').json()
        filter_task_form = FilterTaskForm()
    if request.method == 'POST':
        filter_task_form = FilterTaskForm(request.POST)
        if filter_task_form.is_valid():
            form_parameters = filter_task_form.cleaned_data
            end_point = ROOT_ENDPOINT + 'task/?'
            for key in form_parameters:
                end_point += f'{key}={form_parameters[key]}&'
            tasks = requests.get(end_point).json()

    return render(request, 'task_list.html', {'tasks': tasks[::-1], 'form': filter_task_form})


def task_create_new(request):
    if request.method == 'POST':
        task_creation_form = TaskForm(request.POST)

        if task_creation_form.is_valid():
            end_point = ROOT_ENDPOINT + 'task/'
            task_msg = task_creation_form.cleaned_data
            current_user = request.user.username if request.user.username != '' else 'Anonymous'
            task_msg['author'] = current_user

            requests.post(end_point, task_msg)

            return redirect('task_list')
    else:
        task_creation_form = TaskForm()

    return render(request, 'task_edit.html', {'form': task_creation_form})


def task_details(request, pk):
    task = requests.get(ROOT_ENDPOINT + f'task/{pk}').json()
    return render(request, 'task_details.html', {'task': task})


def task_edit(request, pk):
    task_json = requests.get(ROOT_ENDPOINT + f'task/{pk}').json()
    if request.method == "POST":
        task_edit_form = TaskForm(request.POST)

        if task_edit_form.is_valid():
            end_point = ROOT_ENDPOINT + 'task/{}/'.format(task_json['id'])
            task_msg = task_edit_form.cleaned_data
            current_user = request.user.username if request.user.username != '' else 'Anonymous'
            task_msg['author'] = current_user

            requests.put(end_point, task_msg)

            return redirect('task_details', pk=task_json['id'])
    else:
        task_edit_form = TaskForm()
        for key in task_json:
            if key in task_edit_form.fields:
                task_edit_form.fields[key].initial = task_json[key]

    return render(request, 'task_edit.html', {'form': task_edit_form})


def task_delete(request, pk):
    requests.delete(ROOT_ENDPOINT + f'task/{pk}')
    return redirect('task_list')


def task_history(request):
    task_events_filter = HistoricalTaskEventFilter(request.POST,
                                                   queryset=HistoricalTaskEvent.objects.all().order_by(
                                                       '-occurrence_date'))
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
